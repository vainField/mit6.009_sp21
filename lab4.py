#!/usr/bin/env python3

from util import read_osm_data, great_circle_distance, to_local_kml_url
import pickle

# NO ADDITIONAL IMPORTS!

### HELPER FUNCTIONS/DATA

ALLOWED_HIGHWAY_TYPES = {
    'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified',
    'residential', 'living_street', 'motorway_link', 'trunk_link',
    'primary_link', 'secondary_link', 'tertiary_link',
}


DEFAULT_SPEED_LIMIT_MPH = {
    'motorway': 60,
    'trunk': 45,
    'primary': 35,
    'secondary': 30,
    'residential': 25,
    'tertiary': 25,
    'unclassified': 25,
    'living_street': 10,
    'motorway_link': 30,
    'trunk_link': 30,
    'primary_link': 30,
    'secondary_link': 30,
    'tertiary_link': 25,
}


def unnest(nest):
    '''
    Unnest a nested tuple of paths.
    Each layer contain a node and a subnest.
    The innermost node is the starting point.
    e.g. (c, (b, (a,)))
    '''
    unnested = []
    while nest:   # expand the nested path
        unnested.append(nest[0])
        if len(nest) < 2: break
        nest = nest[1]
    unnested.reverse()
    return unnested


## Uniform-cost Search with Heuristic Function

def heuristic_ucs(start, is_goal, successors, value, heuristic=None):
    
    ### DEFINITION
    '''
    Return the path with minimal value from start node to the goal
    
    Parameters:
        start: start node
        min_val: function to find minimal value in agenda, return a tuple of the path and the value
        is_goal: function to determine if the node is the goal, return a boolean value
        successors: function to find successive nodes and the value to get to them, return a dictionary
        value: function to find the value of node in successors
        heuristic: a heuristic function with default value None
    
    Returns:
        a list of nodes representing the path with minimal value
    '''
    ### MAIN
    ## Helper Functions
    def min_val(agenda, heuristic):
        if heuristic:
            return sorted(
                agenda.items(), 
                key = lambda a: a[1] + heuristic(a[0][0])
            )[0]
        else:
            return sorted(agenda.items(), key = lambda a: a[1])[0]

    ## Main
    expanded = set()
    agenda = {(start,): 0}

    while agenda:
        (path, val) = min_val(agenda, heuristic)
        node = path[0]
        del agenda[path]

        if node not in expanded:
            if is_goal(node):
                return unnest(path)
            expanded.add(node)
            succs = successors(node)
            for s in succs:
                if s not in expanded:
                    new_path = (s, path)
                    new_val = val + value(succs, s)
                    agenda.setdefault(new_path, new_val)
    return None

## Location to Node
def location_node(aux_structures, loc):
    def loc_distance(node):
        return great_circle_distance(loc, node[1])

    node_location = aux_structures['node_location']

    return sorted(node_location.items(), key=loc_distance)[0][0]


### MAIN FUNCTIONS

def build_auxiliary_structures(nodes_filename, ways_filename):
    """
    Create any auxiliary structures you are interested in, by reading the data
    from the given filenames (using read_osm_data)
    """
    # Dictionary of node to tuple of latitude and longitude
    node_loc = {}
    for node in read_osm_data(nodes_filename):
        node_loc.setdefault(node['id'], (node['lat'], node['lon']))

    ## Helper Functions
    # Distance between two nodes
    def dist(node1, node2):
        return great_circle_distance(node_loc[node1], node_loc[node2])
    
    # Add connected nodes to each node in a way. Each connected node has a dictionary of distance and travel time
    def add_connected_nodes(data, nodes, speed, pos):
        if pos == 0: k = 1
        if pos == 1: k = -1
        for i in range(0+pos, len(nodes)-1+pos):
            dist_nodes = dist(nodes[i], nodes[i+k])
            time_nodes = dist_nodes / speed
            if nodes[i] not in data:
                data.setdefault(nodes[i], {nodes[i+k]: {'dist': dist_nodes, 'time': time_nodes}})
            else:
                if nodes[i+k] not in data[nodes[i]]:
                    data[nodes[i]].setdefault(nodes[i+k], {'dist': dist_nodes, 'time': time_nodes})
                else:
                    if dist_nodes < data[nodes[i]][nodes[i+k]]['dist']:
                        data[nodes[i]][nodes[i+k]]['dist'] = dist_nodes
                    if time_nodes < data[nodes[i]][nodes[i+k]]['time']:
                        data[nodes[i]][nodes[i+k]]['time'] = time_nodes
        return data
    
    ## Main
    # Dictionary of node to connected nodes
    node_nodes = {}
    for way in read_osm_data(ways_filename):
        tags = way['tags']
        nodes = way['nodes']
        if 'highway' in tags and tags['highway'] in ALLOWED_HIGHWAY_TYPES:
            if 'maxspeed_mph' in tags:
                speed = tags['maxspeed_mph']
            else:
                speed = DEFAULT_SPEED_LIMIT_MPH[tags['highway']]
            if 'oneway' in tags and tags['oneway'] == 'yes':
                node_nodes = add_connected_nodes(node_nodes, nodes, speed, 0)
            else: 
                node_nodes = add_connected_nodes(node_nodes, nodes, speed, 0)
                node_nodes = add_connected_nodes(node_nodes, nodes, speed, 1)

    # Keep relevant Nodes
    rlvnt_node_loc = {}
    for node in node_nodes:
        rlvnt_node_loc.setdefault(node, node_loc[node])
        for sub_node in node_nodes[node]:
            rlvnt_node_loc.setdefault(sub_node, node_loc[sub_node])

    aux_structures = {'node_location': rlvnt_node_loc, 'node_nodes': node_nodes}
    return aux_structures


def find_short_path_nodes(aux_structures, node1, node2):

    ### DOCUMENTATION
    """
    Return the shortest path between the two nodes

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        node1: node representing the start location
        node2: node representing the end location

    Returns:
        a list of node IDs representing the shortest path (in terms of
        distance) from node1 to node2
    """

    # ## main
    # start = node1
    # end = node2
    # agenda = {(start,): 0}
    # if heuristic:
    #     agenda[(start,)] += great_circle_distance(node_location[start], node_location[end])
    # expanded = set()
    # i = 0

    # while agenda:
    #     (path, dist) = short_path(agenda)
    #     node = path[0]
    #     del agenda[path]

    #     if node not in expanded:
    #         expanded.add(node)
    #         if node == end:
    #             print('total steps:', i)
    #             return unnest(path)
    #         if node in successive_nodes:
    #             succ_nodes = successive_nodes[node]
    #             for s_node in succ_nodes:
    #                 if s_node not in expanded:
    #                     new_path = (s_node, path)
    #                     new_dist = dist + succ_nodes[s_node]['dist']
    #                     if heuristic:
    #                         new_dist += great_circle_distance(node_location[s_node], node_location[end])
    #                     agenda.setdefault(new_path, new_dist)
    # return None

    ### MAIN
    ## Data Aliases
    successive_nodes = aux_structures['node_nodes']
    node_location = aux_structures['node_location']

    ## Helper Functions
    def is_goal(node):
        if node == node2:
            return True
        else:
            return False

    def successors(node):
        if node not in successive_nodes: 
            return {}
        else:
            return successive_nodes[node]

    def value(succs, s):
        return succs[s]['dist']

    def heuristic(node):
        return great_circle_distance(node_location[node], node_location[node2])

    ## Return
    return heuristic_ucs(node1, is_goal, successors, value, heuristic)





def find_short_path(aux_structures, loc1, loc2):

    ### DOCUMENTATION
    """
    Return the shortest path between the two locations

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location
 
    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of distance) from loc1 to loc2.
    """

    ### MAIN
    ## Find closest nodes of locations
    node1 = location_node(aux_structures, loc1)
    node2 = location_node(aux_structures, loc2)

    ## Find shortest path
    nodes = find_short_path_nodes(aux_structures, node1, node2)
    if nodes == None: return None

    ## From node to latitude & longitude
    node_location = aux_structures['node_location']
    path_locations = []
    for node in nodes:
        path_locations.append(node_location[node])
    return path_locations


def find_fast_path(aux_structures, loc1, loc2):

    ### DOCUMENTATION
    """
    Return the shortest path between the two locations, in terms of expected
    time (taking into account speed limits).

    Parameters:
        aux_structures: the result of calling build_auxiliary_structures
        loc1: tuple of 2 floats: (latitude, longitude), representing the start
              location
        loc2: tuple of 2 floats: (latitude, longitude), representing the end
              location

    Returns:
        a list of (latitude, longitude) tuples representing the shortest path
        (in terms of time) from loc1 to loc2.
    """

    ### MAIN
    ## Data Aliases
    successive_nodes = aux_structures['node_nodes']
    node_location = aux_structures['node_location']

    ## Find closest nodes of locations
    node1 = location_node(aux_structures, loc1)
    node2 = location_node(aux_structures, loc2)

    ## Helper Functions
    def is_goal(node):
        if node == node2:
            return True
        else:
            return False

    def successors(node):
        if node not in successive_nodes: 
            return {}
        else:
            return successive_nodes[node]

    def value(succs, s):
        return succs[s]['time']

    ## Find fastest path
    nodes = heuristic_ucs(node1, is_goal, successors, value)
    if nodes == None: return None

    ## From node to latitude & longitude
    path_locations = []
    for node in nodes:
        path_locations.append(node_location[node])
    return path_locations


if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.

    ## TEST

    # print(build_auxiliary_structures('resources/mit.nodes', 'resources/mit.ways'))
    # for way in read_osm_data('resources/mit.ways'):
    #     print(way)
    # for node in read_osm_data('resources/mit.nodes'):
    #     print(node)

    midwest = build_auxiliary_structures('resources/midwest.nodes', 'resources/midwest.ways')
    print(midwest['node_nodes'][272855431])
    node_location = midwest['node_location']

    print(great_circle_distance(node_location[233945564], node_location[234022411]) + 0.04194923026635126)
    print(great_circle_distance(node_location[233945564], node_location[233888931]) + 0.041202743032225174)

    print(great_circle_distance(node_location[272855431], node_location[234022411]))
    print(great_circle_distance(node_location[272855431], node_location[233888931]))

    # with open('test_data/test_midwest_03_short_nodes.pickle', 'rb') as f:
    #     a = pickle.load(f)
    # print(a)

    ## QUESTIONS

    # node_num = 0
    # node_name = 0
    # for node in read_osm_data('resources/cambridge.nodes'):
    #     print(node)
    #     break
    # # {'id': 21321186, 'lat': 42.4839446, 'lon': -71.2195117, 'tags': {}}
    #     if 'name' in node['tags']:
    #         node_name += 1
    #         if node['tags']['name'] == '77 Massachusetts Ave':
    #             print(node['id'])
    #     node_num += 1

    # print(node_num)
    # print(node_name)

    # way_num = 0
    # one_way_num = 0
    # for way in read_osm_data('resources/cambridge.ways'):
    #     print(way)
    #     break
    # # {'id': 4762630, 'nodes': [30416737, 6371042904, 6371042906, 6371042903, 6371042905, 542944353, 542944364, 6370679539, 6370679541, 6370679545, 6370679542, 542944370, 30417567, 6370679540, 30416743, 6370679548, 6370679543, 6370679551, 30416744, 6370682035, 6370682028, 6370682023, 6370682031, 6381501107, 30416745, 6381501106, 6381501103, 6381501094, 6381501112, 30417580, 6381501100, 6381501098, 6381501110, 30417581, 6381501101, 30417582, 6381501108, 6381501111, 60822142, 6381501097, 30417583], 'tags': {'hgv': 'designated', 'ref': 'I 93;US 1', 'foot': 'no', 'horse': 'no', 'lanes': '4', 'oneway': 'yes', 'bicycle': 'no', 'highway': 'motorway', 'surface': 'asphalt', 'maxspeed': '55 mph', 'sidewalk': 'none', 'maxspeed_mph': 55}}
    #     if 'oneway' in way['tags']:
    #         one_way_num += 1
    #         print(way['tags']['oneway'])
    #     way_num += 1

    # print(way_num)
    # print(one_way_num)

    ## 3.1.3

    # print(great_circle_distance((42.363745, -71.100999), (42.361283, -71.239677)))
    # # 7.080591175849026
    # for node in read_osm_data('resources/midwest.nodes'):
    #     if node['id'] == 233941454:
    #         node1_pos = (node['lat'], node['lon'])
    #     if node['id'] == 233947199:
    #         node2_pos = (node['lat'], node['lon'])
    # print(great_circle_distance(node1_pos, node2_pos))
    # # 21.204649112337506

    ## 5.2

    # cambridge_data = build_auxiliary_structures('resources/cambridge.nodes', 'resources/cambridge.ways')
    # loc1 = (42.3858, -71.0783)
    # loc2 = (42.5465, -71.1787)
    # print(find_short_path(cambridge_data, loc1, loc2))
    # # 386255
    # # 76773

    pass
