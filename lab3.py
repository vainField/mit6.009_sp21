#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for this lab will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).

#HELPER FUNCTIONS

def id_together(actor_id_1, actor_id_2):
    '''
    Calculate a distinct tuple of two numbers of two actors' IDs.
    '''
    return (actor_id_1+actor_id_2, abs(actor_id_1-actor_id_2))

def transform_data(raw_data):
    '''
    Raw data is a list of tuples, each of which includes two actors' IDs and the ID of the film they acted together.
    Transform it into a dictionaries of three dictionaries as values.
    1st one with key of id_together and value of film ID.
    2nd one with key of an actor's ID and value of a set of actors' IDs.
    3rd one with key of a film ID and value of a set of actors' IDs.
    '''
    actors_film = {}
    actor_actors = {}
    film_actors = {}

    for i in raw_data:
        assert len(i) == 3, 'transform_data: wrong data type'

        actors_film.setdefault(id_together(i[0], i[1]), i[2])   # 1st dic

        if i[0] not in actor_actors:   # 2nd dic
            actor_actors.setdefault(i[0], {i[1]})
        else:
            actor_actors[i[0]].add(i[1])
        if i[1] not in actor_actors:
            actor_actors.setdefault(i[1], {i[0]})
        else:
            actor_actors[i[1]].add(i[0])

        if i[2] not in film_actors:   # 3rd dic
            film_actors.setdefault(i[2], {i[0], i[1]})
        else:
            film_actors[i[2]].add(i[0])
            film_actors[i[2]].add(i[1])

    trans_data = {'actors_film': actors_film, 'actor_actors': actor_actors, 'film_actors': film_actors}
    return trans_data

def bfs(start, is_goal, succesors):
    agenda = [(start,)]
    seen = {start}
    i = 0
    while agenda:
        if i >= len(agenda): return None
        path = agenda[i]
        node = path[0]
        if is_goal(node):
            return unnest(path)
        for s in succesors(node):
            if s not in seen:
                agenda.append((s, path))
                seen.add(s)
        i += 1

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


#MAIN FUNCTIONS

def acted_together(data, actor_id_1, actor_id_2):
    '''
    Whether two actors have acted together or not. 
    True if two IDs are same.
    '''
    id = id_together(actor_id_1, actor_id_2)
    if id[1] == 0:   # If two IDs are same.
        return True
    elif id in data['actors_film']:   # If id_together is in the actors_film's keys
        return True
    else:
        return False

def actors_with_bacon_number(data, n):
    bacon = 4724
    actors_minus_2 = set()   # actors with (n-2) bacon number
    actors_minus_1 = {bacon,}   # actors with (n-1) bacon number
    for i in range(n):
        successive_actors = set()
        for actor in actors_minus_1:
            successive_actors = set.union(data['actor_actors'][actor], successive_actors)
            successive_actors = successive_actors.difference(set.union(actors_minus_1, actors_minus_2))
        actors_minus_2 = actors_minus_1
        actors_minus_1 = successive_actors
        if actors_minus_1 == set():   # if there's no succesive actors
            return set()
    return actors_minus_1



    # actors_seen = {bacon,}
    # for i in range(n):
    #     successive_actors = set()
    #     for actor in actors_minus_1:
    #         successive_actors = set.union(data['actor_actors'][actor], successive_actors)
    #         successive_actors = successive_actors.difference(actors_seen)
    #     actors_seen = set.union(successive_actors, actors_seen)
    #     if successive_actors == set():
    #         return set()
    # return successive_actors

    ## HOW TO DEAL WITH RECURSION OF PREVIOUS TWO ITEMS -- keep track?

    # if n == -1:
    #     return set()
    # elif n == 0:
    #     return {bacon,}
    # else:
    #     successive_actors = set()
    #     for actor in actors_with_bacon_number(data, n-1):
    #         successive_actors = set.union(data['actor_actors'][actor], successive_actors)
    #     return successive_actors.difference(set.union(
    #         actors_with_bacon_number(data, n-1),
    #         actors_with_bacon_number(data, n-2)
    #     ))

        # return set.union(data['actor_actors'][actor] for actor in actors_with_bacon_number(data, n-1))


def bacon_path(data, actor_id):
    '''
    Find a shortest path from Kevin Bacon to an actor.
    '''
    bacon = 4724
    return actor_to_actor_path(data, bacon, actor_id)

    # assert actor_id != bacon, 'Kevin Bacon self'
    # agenda = [(bacon,)]   # record of paths
    # seen = {bacon}   # actors seen will not be added to new paths
    # i = 0   # No. of path to be examined based on bfs
    # while agenda:
    #     if i >= len(agenda): return None   # if every possible path is examined
    #     path = agenda[i]
    #     current_actor = path[0]
    #     if current_actor == actor_id:
    #         nest = path
    #         unnested = []
    #         while nest:   # expand the nested path
    #             unnested.append(nest[0])
    #             if len(nest) < 2: break
    #             nest = nest[1]
    #         unnested.reverse()
    #         return unnested
    #     for actor in data['actor_actors'][current_actor]:
    #         if actor not in seen:
    #             agenda.append((actor, path))   # appended paths are in a nested format
    #             seen.add(actor)
    #     i += 1
    

def actor_to_actor_path(data, actor_id_1, actor_id_2):
    return actor_path(data, actor_id_1, lambda x: x == actor_id_2)

    # agenda = [(actor_id_1,)]   # record of paths
    # seen = {actor_id_1}   # actors seen will not be added to new paths
    # i = 0   # No. of path to be examined based on bfs
    # while agenda:
    #     if i >= len(agenda): return None   # if every possible path is examined
    #     path = agenda[i]
    #     current_actor = path[0]
    #     if current_actor == actor_id_2:
    #         nest = path
    #         unnested = []
    #         while nest:   # expand the nested path
    #             unnested.append(nest[0])
    #             if len(nest) < 2: break
    #             nest = nest[1]
    #         unnested.reverse()
    #         return unnested
    #     for actor in data['actor_actors'][current_actor]:
    #         if actor not in seen:
    #             agenda.append((actor, path))   # appended paths are in a nested format
    #             seen.add(actor)
    #     i += 1    


def actor_path(data, actor_id_1, goal_test_function):
    def successive_actors(actor):
        return data['actor_actors'][actor]
    return bfs(actor_id_1, goal_test_function, successive_actors)



def actors_connecting_films(data, film1, film2):
    def succesive_actors(actor):
        if actor == film1:
            return data['film_actors'][film1]
        else: return data['actor_actors'][actor]
    return bfs(film1, lambda p: p in data['film_actors'][film2], succesive_actors)[1:]

    


if __name__ == '__main__':
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.

    with open('resources/large.pickle', 'rb') as f:
        largedb = pickle.load(f)
    with open('resources/small.pickle', 'rb') as f:
        smalldb = pickle.load(f)
    with open('resources/tiny.pickle', 'rb') as f:
        tinydb = pickle.load(f)
    
    with open('resources/names.pickle', 'rb') as f:
        namedb = pickle.load(f)
    # print(tinydb)

    # print(namedb['Stephen Hogan'])

    # for actor_name in namedb:
    #     if namedb[actor_name] == 5177:
    #         print(actor_name)
    #         break

    path_num = bacon_path(transform_data(largedb), namedb['Roberto Dell\'Acqua'])
    print(path_num)
    path_name = []
    for num in path_num:
        for name, numb in namedb.items():
            if numb == num: path_name.append(name)
    print(path_name)

    # print([name for name, num in namedb.items() if num in bpath])


    pass