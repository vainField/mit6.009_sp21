#!/usr/bin/env python3
"""6.009 Lab -- Six Double-Oh Mines"""

# NO IMPORTS ALLOWED!

from typing import Collection


## HELPER FUNCTIONS

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f'{key}:')
            for inner in val:
                print(f'    {inner}')
        else:
            print(f'{key}:', val)

# CREATE SAME-ELEMENT MATRIX
def init_matrix(value, num_rows, num_cols):
    '''
    Create a matrix with a same element.

    Parameters:
        value: the element in the matrix
        num_rows: number of rows
        num_cols: number of columns

    Returns:
        A matrix
    '''
    return [[value] * num_cols for _ in range(num_rows)]

# FINDING NEIGHBOR CELLS
def neighbor_cells(row, col, num_rows, num_cols):
    '''
    Find neighbor cells.

    Parameters:
        row: current row
        col: current column
        num_rows: number of rows
        num_cols: number of columns

    Returns:
        A list of cells, given in (row, column) pairs, which are tuples. 
    '''
    result = []
    if row != 0: 
        result.append((row-1, col))
        if col != 0: 
            result.append((row-1, col-1))
        if col != num_cols-1: 
            result.append((row-1, col+1))
    if row != num_rows-1: 
        result.append((row+1, col))
        if col != 0: 
            result.append((row+1, col-1))
        if col != num_cols-1: 
            result.append((row+1, col+1))
    if col != 0: 
        result.append((row, col-1))
    if col != num_cols-1: 
        result.append((row, col+1))

    return result


## MAIN FUNCTIONS

# 2-D IMPLEMENTATION

def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: 3
    dimensions: (2, 4)
    mask:
        [False, False, False, False]
        [False, False, False, False]
    revealed: 0
    state: ongoing
    """

    mask = init_matrix(False, num_rows, num_cols)
    board = init_matrix(0, num_rows, num_cols)

    for (row, col) in bombs:
        for cell in neighbor_cells(row, col, num_rows, num_cols):
            board[cell[0]][cell[1]] += 1

    for (row, col) in bombs:
        board[row][col] = '.'
    
    num_bombs = len(bombs)

    return {
        'dimensions': (num_rows, num_cols),
        'board' : board,
        'mask' : mask,
        'bombs' : num_bombs,
        'revealed': 0,
        'state': 'ongoing'}

    # board = []
    # for r in range(num_rows):
    #     row = []
    #     for c in range(num_cols):
    #         if [r,c] in bombs or (r,c) in bombs:
    #             row.append('.')
    #         else:
    #             row.append(0)
    #     board.append(row)
    # mask = []
    # for r in range(num_rows):
    #     row = []
    #     for c in range(num_cols):
    #         row.append(False)
    #     mask.append(row)
    # for r in range(num_rows):
    #     for c in range(num_cols):
    #         if board[r][c] == 0:
    #             neighbor_bombs = 0
    #             if 0 <= r-1 < num_rows:
    #                 if 0 <= c-1 < num_cols:
    #                     if board[r-1][c-1] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r < num_rows:
    #                 if 0 <= c-1 < num_cols:
    #                     if board[r][c-1] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r+1 < num_rows:
    #                 if 0 <= c-1 < num_cols:
    #                     if board[r+1][c-1] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r-1 < num_rows:
    #                 if 0 <= c < num_cols:
    #                     if board[r-1][c] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r < num_rows:
    #                 if 0 <= c < num_cols:
    #                     if board[r][c] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r+1 < num_rows:
    #                 if 0 <= c < num_cols:
    #                     if board[r+1][c] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r-1 < num_rows:
    #                 if 0 <= c+1 < num_cols:
    #                     if board[r-1][c+1] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r < num_rows:
    #                 if 0 <= c+1 < num_cols:
    #                     if board[r][c+1] == '.':
    #                         neighbor_bombs += 1
    #             if 0 <= r+1 < num_rows:
    #                 if 0 <= c+1 < num_cols:
    #                     if board[r+1][c+1] == '.':
    #                         neighbor_bombs += 1
    #             board[r][c] = neighbor_bombs


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['mask'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is visible on the board after digging (i.e. game['mask'][bomb_location] ==
    True), 'victory' when all safe squares (squares that do not contain a bomb)
    and no bombs are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'bombs': 3,
    ...         'revealed': 1,
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: 3
    dimensions: (2, 4)
    mask:
        [False, True, True, True]
        [False, False, True, True]
    revealed: 5
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'bombs': 3,
    ...         'revealed': 1,
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: 3
    dimensions: [2, 4]
    mask:
        [True, True, False, False]
        [False, False, False, False]
    revealed: 2
    state: defeat
    """

    ## ALIASES
    dim = game['dimensions']
    board = game['board']
    mask = game['mask']
    state = game['state']

    ## MAIN
    revealed = 0

    if state == 'defeat' or state == 'victory':   # game end
        return revealed

    if mask[row][col] != True:   # dig an unrevealed cell
        mask[row][col] = True
        revealed += 1
        game['revealed'] += 1
    else:                       # dig a revealed cell
        return 0

    if board[row][col] == '.':   # dig a bomb
        game['state'] = 'defeat'
        return revealed

    if game['revealed'] + game['bombs'] == dim[0] * dim[1]:   # digged all non-bomb cells
        game['state'] = 'victory'
        return revealed

    if board[row][col] == 0:   # dig a cell with no adjacent bomb
        for cell in neighbor_cells(row, col, dim[0], dim[1]):
            if mask[cell[0]][cell[1]] == False:
                revealed += dig_2d(game, cell[0], cell[1])   # dig its adjacent cells
        return revealed
    else: return revealed

    # bombs = 0
    # covered_squares = 0
    # for r in range(game['dimensions'][0]):
    #     for c in range(game['dimensions'][1]):
    #         if game['board'][r][c] == '.':
    #             if  game['mask'][r][c] == True:
    #                 bombs += 1
    #         elif game['mask'][r][c] == False:
    #             covered_squares += 1
    # if bombs != 0:
    #     # if bombs is not equal to zero, set the game state to defeat and
    #     # return 0
    #     game['state'] = 'defeat'
    #     return 0
    # if covered_squares == 0:
    #     game['state'] = 'victory'
    #     return 0

    # if game['mask'][row][col] != True:
    #     game['mask'][row][col] = True
    #     revealed = 1
    # else:
    #     return 0

    # if game['board'][row][col] == 0:
    #     num_rows, num_cols = game['dimensions']
    #     if 0 <= row-1 < num_rows:
    #         if 0 <= col-1 < num_cols:
    #             if game['board'][row-1][col-1] != '.':
    #                 if game['mask'][row-1][col-1] == False:
    #                     revealed += dig_2d(game, row-1, col-1)
    #     if 0 <= row < num_rows:
    #         if 0 <= col-1 < num_cols:
    #             if game['board'][row][col-1] != '.':
    #                 if game['mask'][row][col-1] == False:
    #                     revealed += dig_2d(game, row, col-1)
    #     if 0 <= row+1 < num_rows:
    #         if 0 <= col-1 < num_cols:
    #             if game['board'][row+1][col-1] != '.':
    #                 if game['mask'][row+1][col-1] == False:
    #                     revealed += dig_2d(game, row+1, col-1)
    #     if 0 <= row-1 < num_rows:
    #         if 0 <= col < num_cols:
    #             if game['board'][row-1][col] != '.':
    #                 if game['mask'][row-1][col] == False:
    #                     revealed += dig_2d(game, row-1, col)
    #     if 0 <= row < num_rows:
    #         if 0 <= col < num_cols:
    #             if game['board'][row][col] != '.':
    #                 if game['mask'][row][col] == False:
    #                     revealed += dig_2d(game, row, col)
    #     if 0 <= row+1 < num_rows:
    #         if 0 <= col < num_cols:
    #             if game['board'][row+1][col] != '.':
    #                 if game['mask'][row+1][col] == False:
    #                     revealed += dig_2d(game, row+1, col)
    #     if 0 <= row-1 < num_rows:
    #         if 0 <= col+1 < num_cols:
    #             if game['board'][row-1][col+1] != '.':
    #                 if game['mask'][row-1][col+1] == False:
    #                     revealed += dig_2d(game, row-1, col+1)
    #     if 0 <= row < num_rows:
    #         if 0 <= col+1 < num_cols:
    #             if game['board'][row][col+1] != '.':
    #                 if game['mask'][row][col+1] == False:
    #                     revealed += dig_2d(game, row, col+1)
    #     if 0 <= row+1 < num_rows:
    #         if 0 <= col+1 < num_cols:
    #             if game['board'][row+1][col+1] != '.':
    #                 if game['mask'][row+1][col+1] == False:
    #                     revealed += dig_2d(game, row+1, col+1)

    # bombs = 0  # set number of bombs to 0
    # covered_squares = 0
    # for r in range(game['dimensions'][0]):
    #     # for each r,
    #     for c in range(game['dimensions'][1]):
    #         # for each c,
    #         if game['board'][r][c] == '.':
    #             if  game['mask'][r][c] == True:
    #                 # if the game mask is True, and the board is '.', add 1 to
    #                 # bombs
    #                 bombs += 1
    #         elif game['mask'][r][c] == False:
    #             covered_squares += 1
    # bad_squares = bombs + covered_squares
    # if bad_squares > 0:
    #     game['state'] = 'ongoing'
    #     return revealed
    # else:
    #     game['state'] = 'victory'
    #     return revealed


def render_2d(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring bombs).
    game['mask'] indicates which squares should be visible.  If xray is True (the
    default is False), game['mask'] is ignored and all cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A 2D array (list of lists)

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'mask':  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    ### ALIASES
    mask = game['mask']
    board = game['board']
    dim = game['dimensions']

    ### MAIN
    
    if xray == True:
        result = [[' '] * dim[1] for _ in range(dim[0])]
        for row in range(dim[0]):
            for col in range(dim[1]):
                if board[row][col] != 0:
                    result[row][col] = str(board[row][col])
        return result
    else:
        result = [['_'] * dim[1] for _ in range(dim[0])]
        for row in range(dim[0]):
            for col in range(dim[1]):
                if mask[row][col] == True:
                    if board[row][col] == 0:
                        result[row][col] = ' '
                    else:
                        result[row][col] = str(board[row][col])
        return result
    



def render_ascii(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function 'render_2d(game)'.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['mask']

    Returns:
       A string-based representation of game

    >>> print(render_ascii({'dimensions': (2, 4),
    ...                     'state': 'ongoing',
    ...                     'board': [['.', 3, 1, 0],
    ...                               ['.', '.', 1, 0]],
    ...                     'mask':  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """

    ## ALIASES
    dim = game['dimensions']

    ## MAIN
    result = render_2d(game, xray)
    return '\n'.join(''.join(result[row][:]) for row in range(dim[0]))

# '\n'.join('%s' % ''.join(result[row][:]) for row in range(dim[0]))

# N-D IMPLEMENTATION

# HELPER FUNCTIONS

def get_value(array, coordinate):
    '''
    Given an N-d array and a tuple/list of coordinates, returns the value at those coordinates in the array.

    >>> get_value([[1,2], [3,4]], [1,1])
    4

    >>> get_value([[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]], [1, 0, 1])
    6

    '''
    # print('array:', array)
    # print('coordinate:', coordinate)

    if len(coordinate) == 1:
        return array[coordinate[0]]
    return get_value(
        array[coordinate[0]],
        coordinate[1:]
    )

def change_value(array, coordinate, value):
    '''
    Given an N-d array, a tuple/list of coordinates, and a value, replaces the value at those coordinates in the array with the given value.

    >>> a = [[1, 2], [3, 4]]
    >>> change_value(a, [1, 1], 5)
    >>> print(a)
    [[1, 2], [3, 5]]
    '''
    if len(coordinate) == 1:
        array[coordinate[0]] = value
    else:
        change_value(
            array[coordinate[0]],
            coordinate[1:],
            value
        )

def init_array(dim, value):
    '''
    Given a list of dimensions and a value, creates a new N-d array with those dimensions, where each value in the array is the given value.

    >>> init_array((2, 3), 1)
    [[1, 1, 1], [1, 1, 1]]
    '''
    nd = len(dim)
    if nd == 1:
        return [value] * dim[0]
    else:
        return [init_array(dim[1:], value) for _ in range(dim[0])]

def neighbors(dim, coordinate):
    '''
    A function that returns all the neighbors of a given tuple of coordinates in a given dimension of array.

    Parameters:
        dim (tuple): The dimension of the array
        coordinate (tuple): The coordinate whose neighbors are being searched
    
    Returns:
        a set of tuples, each an N-dimensional coordinate

    >>> neighbors((3,), (0,))
    {(0,), (1,)}
    >>> neighbors((2, 3), (0, 0))
    {(1, 0), (0, 1), (1, 1), (0, 0)} 
    '''
    coord = coordinate[0]
    if len(dim) == 1:
        if dim[0] == 1:
            assert coord == 0, 'wrong input'
            return {(coord,)}
        if coord == 0:
            return {(coord,), (coord + 1,)}
        elif coord == dim[0] - 1:
            return {(coord - 1,), (coord,)}
        else:
            return {(coord - 1,), (coord,), (coord + 1,)}
    else:
        sub_neighbors = neighbors(dim[1:], coordinate[1:])
        former = {i + (coord - 1,) for i in sub_neighbors}
        current = {i + (coord,) for i in sub_neighbors}
        latter = {i + (coord + 1,) for i in sub_neighbors}
        if dim[0] == 1:
            assert coord == 0, 'wrong input'
            return current
        if coord == 0:
            return set.union(current, latter)
        elif coord == dim[0] - 1:
            return set.union(former, current)
        else:
            return set.union(format, current, latter)

def gen_neighbors(dim, coordinate):
    '''
    A function that generates all the neighbors of a given tuple of coordinates in a given dimension of array.

    Parameters:
        dim (tuple): The dimension of the array
        coordinate (tuple): The coordinate whose neighbors are being searched
    
    Returns:
        a tupe at a time, each an N-dimensional coordinate

    >>> f = gen_neighbors((3,), (0,))
    >>> f.__next__()
    (0,)
    >>> f.__next__()
    (1,)
    >>> f = gen_neighbors((2, 3), (0, 0))
    >>> f.__next__()
    (0, 0)
    >>> f.__next__()
    (0, 1)
    '''

    coord = coordinate[0]
    if len(dim) == 1:
        if coord == 0:
            for i in range(2):
                yield (coord + i,)
        elif coord == dim[0] - 1:
            for i in range(-1, 1):
                yield (coord + i,)
        else:
            for i in range(-1, 2):
                yield (coord + i,)
    else:
        if coord == 0:
            for j in range(2):
                for i in gen_neighbors(dim[1:], coordinate[1:]):
                    yield (coord + j,) + i
        elif coord == dim[0] - 1:
            for j in range(-1, 1):
                for i in gen_neighbors(dim[1:], coordinate[1:]):
                    yield (coord + j,) + i
        else:
            for j in range(-1, 2):
                for i in gen_neighbors(dim[1:], coordinate[1:]):
                    yield (coord + j,) + i

def gen_coordinate(dim):
    '''
    A function that yields all possible coordinates in a given board.

    Parameters:
        dim: Dimensions of the board

    Returns:
        a tupe at a time, each an N-dimensional coordinate

    >>> f = gen_coordinate((3,))
    >>> f.__next__()
    (0,)
    >>> f.__next__()
    (1,)
    >>> f = gen_coordinate((3, 4))
    >>> f.__next__()
    (0, 0)
    >>> f.__next__()
    (0, 1)
    '''
    nd_current = dim[0]
    if len(dim) == 1:
        for i in range(nd_current):
            yield (i,)
    else:
        for j in range(nd_current):
            for i in gen_coordinate(dim[1:]):
                yield (j,) + i

def array_size(dim):
    '''
    Given an array dimension, return the element number in the array. (int)
    '''
    if len(dim) == 1:
        return dim[0]
    else:
        return dim[0] * array_size(dim[1:])

# MAIN FUNCTIONS

def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'mask' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of lists, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: 3
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    revealed: 0
    state: ongoing
    """
    mask = init_array(dimensions, False)
    board = init_array(dimensions, 0)

    for coordinate in bombs:
        # print('bomb:', coordinate)
        for cell in gen_neighbors(dimensions, coordinate):
            # print('neighbor:', cell)
            change_value(board, cell, get_value(board, cell) + 1)

    for coordinate in bombs:
        change_value(board, coordinate, '.')

    num_bombs = len(bombs)

    return {
        'dimensions': dimensions,
        'board': board,
        'mask': mask,
        'bombs': num_bombs,
        'revealed': 0,
        'state': 'ongoing'
    }





    # mask = init_matrix(False, num_rows, num_cols)
    # board = init_matrix(0, num_rows, num_cols)

    # for (row, col) in bombs:
    #     for cell in neighbor_cells(row, col, num_rows, num_cols):
    #         board[cell[0]][cell[1]] += 1

    # for (row, col) in bombs:
    #     board[row][col] = '.'
    
    # num_bombs = len(bombs)

    # return {
    #     'dimensions': (num_rows, num_cols),
    #     'board' : board,
    #     'mask' : mask,
    #     'bombs' : num_bombs,
    #     'revealed': 0,
    #     'state': 'ongoing'}


def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the mask to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'bombs': 3,
    ...      'revealed': 1,
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: 3
    dimensions: (2, 4, 2)
    mask:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    revealed: 9
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    ...               [[False, False], [False, False], [False, False], [False, False]]],
    ...      'bombs': 3,
    ...      'revealed': 1,
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: 3
    dimensions: (2, 4, 2)
    mask:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    revealed: 2
    state: defeat




    >>> game = new_game_nd((3,3,2),[(1,2,0)])
    >>> dump(game)
    board:
        [[0, 0], [1, 1], [1, 1]]
        [[0, 0], [1, 1], ['.', 1]]
        [[0, 0], [1, 1], [1, 1]]
    dimensions: (3, 3, 2)
    mask:
        [[False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False]]
    state: ongoing
    >>> dig_nd(game, (2,1,0))
    1
    >>> dump(game)
    board:
        [[0, 0], [1, 1], [1, 1]]
        [[0, 0], [1, 1], ['.', 1]]
        [[0, 0], [1, 1], [1, 1]]
    dimensions: (3, 3, 2)
    mask:
        [[False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False]]
        [[False, False], [True, False], [False, False]]
    state: ongoing
    >>> dig_nd(game, (0,0,0))
    11
    >>> dump(game)
    board:
        [[0, 0], [1, 1], [1, 1]]
        [[0, 0], [1, 1], ['.', 1]]
        [[0, 0], [1, 1], [1, 1]]
    dimensions: (3, 3, 2)
    mask:
        [[True, True], [True, True], [False, False]]
        [[True, True], [True, True], [False, False]]
        [[True, True], [True, True], [False, False]]
    state: ongoing
    >>> dig_nd(game, (1,2,0))
    1
    >>> dump(game)
    board:
        [[0, 0], [1, 1], [1, 1]]
        [[0, 0], [1, 1], ['.', 1]]
        [[0, 0], [1, 1], [1, 1]]
    dimensions: (3, 3, 2)
    mask:
        [[True, True], [True, True], [False, False]]
        [[True, True], [True, True], [True, False]]
        [[True, True], [True, True], [False, False]]
    state: defeat
    """

    ## ALIASES
    dim = game['dimensions']
    board = game['board']
    mask = game['mask']
    state = game['state']

    ## MAIN
    revealed = 0

    if state == 'defeat' or state == 'victory':   # game end
        return revealed

    if get_value(mask, coordinates) != True:   # dig an unrevealed cell
        change_value(mask, coordinates, True)
        revealed += 1
        game['revealed'] += 1
    else:                       # dig a revealed cell
        return 0
    
    if get_value(board, coordinates) == '.':   # dig a bomb
        game['state'] = 'defeat'
        return revealed
    
    if game['revealed'] + game['bombs'] == array_size(dim):   # digged all non-bomb cells
        game['state'] = 'victory'
        return revealed

    if get_value(board, coordinates) == 0:   # dig a cell with no adjacent bomb
        for cell in gen_neighbors(dim, coordinates):
            if get_value(mask, cell) == False:
                revealed += dig_nd(game, cell)   # dig its adjacent cells
        return revealed
    else: return revealed




    # ## ALIASES
    # dim = game['dimensions']
    # board = game['board']
    # mask = game['mask']
    # state = game['state']

    # ## MAIN
    # revealed = 0

    # if state == 'defeat' or state == 'victory':   # game end
    #     return revealed

    # if mask[row][col] != True:   # dig an unrevealed cell
    #     mask[row][col] = True
    #     revealed += 1
    #     game['revealed'] += 1
    # else:                       # dig a revealed cell
    #     return 0

    # if board[row][col] == '.':   # dig a bomb
    #     game['state'] = 'defeat'
    #     return revealed

    # if game['revealed'] + game['bombs'] == dim[0] * dim[1]:   # digged all non-bomb cells
    #     game['state'] = 'victory'
    #     return revealed

    # if board[row][col] == 0:   # dig a cell with no adjacent bomb
    #     for cell in neighbor_cells(row, col, dim[0], dim[1]):
    #         if mask[cell[0]][cell[1]] == False:
    #             revealed += dig_2d(game, cell[0], cell[1])   # dig its adjacent cells
    #     return revealed
    # else: return revealed


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares
    neighboring bombs).  The mask indicates which squares should be
    visible.  If xray is True (the default is False), the mask is ignored
    and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    the mask

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'mask': [[[False, False], [False, True], [True, True], [True, True]],
    ...               [[False, False], [False, False], [True, True], [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """

    ### ALIASES
    mask = game['mask']
    board = game['board']
    dim = game['dimensions']

    ### MAIN
    
    if xray == True:
        result = init_array(dim, ' ')
        for coord in gen_coordinate(dim):
            value = get_value(board, coord)
            if value != 0:
                change_value(result, coord, str(value))
        return result
    else:
        result = init_array(dim, '_')
        for coord in gen_coordinate(dim):
            value = get_value(board, coord)
            uncovered = get_value(mask, coord)
            if uncovered == True:
                if value == 0:
                    change_value(result, coord, ' ')
                else:
                    change_value(result, coord, str(value))
        return result


if __name__ == "__main__":
    ### Test with doctests. Helpful to debug individual lab.py functions.
    # import doctest
    # _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # doctest.testmod(optionflags=_doctest_flags) #runs ALL doctests

    ### SELF_TEST
    # print(render_ascii(new_game_2d(2, 2, [(0, 0)])))

    # import os
    # import pickle
    # TEST_DIRECTORY = os.path.dirname(__file__)
    # test = 0
    # exp_fname = os.path.join(TEST_DIRECTORY, 'test_outputs', f'test2d_integration_{test:02d}.pickle')
    # inp_fname = os.path.join(TEST_DIRECTORY, 'test_inputs', f'test2d_integration_{test:02d}.pickle')
    # with open(inp_fname, 'rb') as f:
    #     inputs = pickle.load(f)
    # with open(exp_fname, 'rb') as f:
    #     expected = pickle.load(f)
    # for location, exp in zip(inputs[1], expected):
    #     num, g, render, renderx, ascii_, ascii_x = exp
    #     print('location:', location, '\n', 'num:', num, '\n', 'g:', g)
    
    # print('input:', input)
    # print('expected:', expected)

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d or any other function you might want.  To do so, comment
    # out the above line, and uncomment the below line of code. This may be
    # useful as you write/debug individual doctests or functions.  Also, the
    # verbose flag can be set to True to see all test results, including those
    # that pass.
    #
    # doctest.run_docstring_examples(dig_nd, globals(), optionflags=_doctest_flags, verbose=False)

    # g = {'dimensions': (2, 4, 2),
    #      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    #                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    #      'mask': [[[False, False], [False, True], [False, False], [False, False]],
    #               [[False, False], [False, False], [False, False], [False, False]]],
    #      'bombs': 3,
    #      'revealed': 1,
    #      'state': 'ongoing'}
    # dig_nd(g, (0, 3, 0))
    # dump(g)

    # game = new_game_nd((3,3,2),[(1,2,0)])

    # a = init_array((3, 3, 2), 0)
    # get_value(a, (2, 1, 0))

    pass