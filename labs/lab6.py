#!/usr/bin/env python3
"""6.009 Lab 6 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS

## HELPER FUNCTIONS

def updating(formula, assignment):
    """
    Updating a formula after a variable assignment.

    >>> f = [
    ...     [('a', True), ('b', True), ('c', True)],
    ...     [('a', False), ('f', True)],
    ...     [('d', False), ('e', True), ('a', True), ('g', True)],
    ...     [('h', False), ('c', True), ('a', False), ('f', True)],
    ... ]
    >>> a = ('a', True)
    >>> updating(f, a)
    [[('f', True)], [('h', False), ('c', True), ('f', True)]]
    >>> b = ('f', False)
    >>> new_f = updating(f, a)
    >>> updating(new_f, b)
    'falsifies'
    """
    if formula == []: return []

    reversed = (assignment[0], not assignment[1])
    new_formula = []

    for clause in formula:
        if len(clause) == 1:
            if clause[0] == reversed:   # contradiction
                return 'falsifies'

        new_clause = clause.copy()
        if assignment in clause:
            continue
        else:
            while reversed in new_clause:
                new_clause.remove(reversed)
            new_formula.append(new_clause)
    return new_formula

    

## MAIN FUNCTIONS
def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])

    >>> f = [
    ...     [('a', True), ('b', True), ('c', True)],
    ...     [('a', False), ('f', True)],
    ...     [('d', False), ('e', True), ('a', True), ('g', True)],
    ...     [('h', False), ('c', True), ('a', False), ('f', True)],
    ... ]
    >>> satisfying_assignment(f)
    {'a': True, 'f': True}
    """
    if formula == []: return {}   # base case

    assignment = {}
    formula = sorted(formula, key=lambda x: len(x))

    # Aliases
    var = formula[0][0][0]

    if len(formula[0]) == 1:   # if a one literal clause exists
        new_formula = updating(formula, formula[0][0])
        if new_formula == 'falsifies':
            return None
        else:
            sub_assignment = satisfying_assignment(new_formula)
            if sub_assignment == None:
                return None
            else:
                assignment.setdefault(var, formula[0][0][1])
                assignment.update(sub_assignment)
                return assignment
    else:
        for bool in [True, False]:
            new_formula = updating(formula, (var, bool))
            if new_formula == 'falsifies':
                continue
            else:
                sub_assignment = satisfying_assignment(new_formula)
                if sub_assignment == None:
                    continue
                else:
                    assignment.setdefault(var, bool)
                    assignment.update(sub_assignment)
                    return assignment
        return None

## SCHEDULING

# Helper Functions
def rule1(student_preferences):
    """
    >>> student_preferences = {'Alice': {'basement', 'penthouse'}, 'Bob': {'kitchen'}, 'Charles': {'basement', 'kitchen'}, 'Dana': {'kitchen', 'penthouse', 'basement'}}
    >>> rule1(student_preferences)
    [[('Alice_penthouse', True), ('Alice_basement', True)], [('Bob_kitchen', True)], [('Charles_basement', True), ('Charles_kitchen', True)], [('Dana_penthouse', True), ('Dana_basement', True), ('Dana_kitchen', True)]]
    """
    rule = []   # every student is given a room that they selected as one of their preferences 
    for student, rooms in student_preferences.items():
        rule.append([(f'{student}_{room}', True) for room in rooms])
    return rule

def rule2(students, rooms):
    """
    >>> students = ['Alice', 'Bob', 'Charles']
    >>> rooms = ['basement', 'kitchen', 'penthouse']
    >>> rule2(students, rooms)
    [[('Alice_basement', False), ('Alice_kitchen', False)], [('Alice_basement', False), ('Alice_penthouse', False)], [('Alice_kitchen', False), ('Alice_penthouse', False)], [('Bob_basement', False), ('Bob_kitchen', False)], [('Bob_basement', False), ('Bob_penthouse', False)], [('Bob_kitchen', False), ('Bob_penthouse', False)], [('Charles_basement', False), ('Charles_kitchen', False)], [('Charles_basement', False), ('Charles_penthouse', False)], [('Charles_kitchen', False), ('Charles_penthouse', False)]]
    """
    rule = []
    for student in students:
        for i in range(len(rooms) - 1):
            rule += [[(f'{student}_{rooms[i]}', False), (f'{student}_{other_room}', False)] for other_room in rooms[i + 1:]]
    return rule

def rule3(students, room_capacities):
    """
    >>> students = ['Alice', 'Bob', 'Charles']
    >>> room_capacities = {'basement': 1, 'kitchen': 2, 'penthouse': 4}
    >>> rule3(students, room_capacities)
    [[('Alice_basement', False), ('Bob_basement', False)], [('Alice_basement', False), ('Charles_basement', False)], [('Bob_basement', False), ('Charles_basement', False)], [('Alice_kitchen', False), ('Bob_kitchen', False), ('Charles_kitchen', False)]]
    """
    rule = []
    for room, capacity in room_capacities.items():
        rule += [clause for clause in room_with_capacity(capacity, room, students)]
    return rule

def room_with_capacity(n, room, students):
    """
    >>> students = ['Alice', 'Bob', 'Charles']
    >>> room = 'basement'
    >>> n = 1
    >>> [i for i in room_with_capacity(n, room, students)]
    [[('Alice_basement', False), ('Bob_basement', False)], [('Alice_basement', False), ('Charles_basement', False)], [('Bob_basement', False), ('Charles_basement', False)]]
    """
    all_literals = [(f'{student}_{room}', False) for student in students]
    num_student = len(students)
    if n == 0:   ## no capacity
        for literal in all_literals:
            yield [literal]
    if n >= len(students):   ## room capacity larger than student number
        return []
    if n < 0:   ## stop iteration
        return

    for sub_clause in room_with_capacity(n-1, room, students):   ## recursion
        index = all_literals.index(sub_clause[-1]) + 1
        if index <= num_student:
            for literal in all_literals[index:]:
                clause = sub_clause + [literal]
                yield clause

# Main
def boolify_scheduling_problem(student_preferences, room_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of room names (strings) that work for that student

    room_capacities: a dictionary mapping each room name to a positive integer
                     for how many students can fit in that room

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up

    We assume no student or room names contain underscores.
    """
    students = [student for student in student_preferences]
    rooms = [room for room in room_capacities]

    return rule1(student_preferences) + rule2(students, rooms) + rule3(students, room_capacities)


if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    # # doctest.testmod(optionflags=_doctest_flags)
    doctest.run_docstring_examples(rule3, globals(), optionflags=_doctest_flags, verbose=False)
    
    
    # f = [
    #     [("a", True), ("a", False)],
    #     [("b", True), ("a", True)],
    #     [("b", True)],
    #     [("b", False),("b", False),("a", False)], 
    #     [("c",True),("d",True)], 
    #     [("c",True),("d",True)]
    # ]
    # print(satisfying_assignment(f))
    

    pass

