# <u>Lab6. SAT Solver</u>

## Conjunctive Normal Form(CNF, 合取范式)

- a *literal* is a variable or the `not` of a variable
- a *clause* is a multi-way `or` of literals
- a CNF *formula* is a multi-way `and` of clauses

### Python Representation

- a *variable* as a Python string
- a *literal* as a pair (a tuple), containing a variable and a Boolean value (`False` if `not` appears in this literal, `True` otherwise)
- a *clause* as a list of literals
- a *formula* as a list of clauses

## Backtracking Search for CNF formula

### Helper Functions

updating a formula based on a new assignment

## Scheduling by Reduction

- In general, it's possible to write a new implementation of backtracking search for each new problem we encounter.
- Another strategy is to *reduce* a new problem to one that we already know how to solve well. 
- Boolean satisfiability is a popular target for reductions, because a lot of effort has gone into building fast SAT solvers.

e.g.

```python
student_preferences = {'Alice': {'basement', 'penthouse'}, 'Bob': {'kitchen'}, 'Charles': {'basement', 'kitchen'}, 'Dana': {'kitchen', 'penthouse', 'basement'}
room_capacities = {'basement': 1, 'kitchen': 2, 'penthouse': 4}
boolify_scheduling_problem(student_preferences, room_capacities)
```

### Encoding the Rules

1. Students Only In Desired Sessions

   ```python
   [
     [('Alice_penthouse', True), ('Alice_basement', True)], 
     [('Bob_kitchen', True)], 
   	[('Charles_basement', True), ('Charles_kitchen', True)], 
     [('Dana_penthouse', True), ('Dana_basement', True), ('Dana_kitchen', True)]
   ]
   ```

2. Each Student In Exactly One Session

   - each student must be in at least one room(encoded in rule1)
   - each student must be in at most one room.

   ```python
   [
     [('Alice_basement', False), ('Alice_kitchen', False)], 
    	[('Alice_basement', False), ('Alice_penthouse', False)], 
    	[('Alice_kitchen', False), ('Alice_penthouse', False)], 
    	[('Bob_basement', False), ('Bob_kitchen', False)], 
    	[('Bob_basement', False), ('Bob_penthouse', False)], 
    	[('Bob_kitchen', False), ('Bob_penthouse', False)], 
    	[('Charles_basement', False), ('Charles_kitchen', False)], 
    	[('Charles_basement', False), ('Charles_penthouse', False)], 
    	[('Charles_kitchen', False), ('Charles_penthouse', False)]
   ]
   ```

3. No Oversubscribed Sessions

   ```python
   [
     [('Alice_basement', False), ('Bob_basement', False)], 
     [('Alice_basement', False), ('Charles_basement', False)], 
     [('Bob_basement', False), ('Charles_basement', False)], 
     [('Alice_kitchen', False), ('Bob_kitchen', False), ('Charles_kitchen', False)]
   ]
   ```

   ## *Thinking*

   Lab6主要讨论了Backtracking Search（回溯搜寻），作为Recursion（递归）的一个例子。在做lab的过程中获得了一个应对大型复杂问题的经验：

   - 将复杂问题拆开为一些小问题，并写为helper functions，除了重复利用外，一个重要的好处是每个function可以单独做test（比如使用doctest）



