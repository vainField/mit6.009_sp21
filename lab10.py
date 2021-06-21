"""6.009 Lab 10: Snek Interpreter Part 2"""


###########
# Imports #
###########

import sys
sys.setrecursionlimit(5000)
import doctest
import operator as op


###########################
# Snek-related Exceptions #
###########################

class SnekError(Exception):
    """
    A type of exception to be raised if there is an error with a Snek
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """
    pass

class SnekSyntaxError(SnekError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """
    pass

class SnekNameError(SnekError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """
    pass

class SnekEvaluationError(SnekError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SnekNameError.
    """
    pass


############################
# Tokenization and Parsing #
############################

def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Snek
                      expression
    
    >>> tokenize("(foo (bar 3.14))")
    ['(', 'foo', '(', 'bar', '3.14', ')', ')']
    >>> tokenize("(cat (dog (tomato)))")
    ['(', 'cat', '(', 'dog', '(', 'tomato', ')', ')', ')']
    >>> tokenize("cat")
    ['cat']
    >>> tokenize("3.14")
    ['3.14']
    """
    out = []
    token = ''
    source += ' '  ## for recognition of single element source

    i = 0
    while source[i:]:
        t = source[i]
        if t == ';':  ## comment
            i += 1
            while source[i:] and source[i] != '\n':  ## end of source or line
                i += 1
        elif t == '\n' or t == ' ':  ## need to check if its after a symbol
            if token != '':
                out.append(token)
                token = ''
        elif t == '(':
            out.append(t)
        elif t == ')':  ## need to check if its after a symbol
            if token != '':
                out.append(token)
                token = ''
            out.append(t)
        else:   ## character or int or operator or '.' (can be continuous)
            token += t
        i += 1
    return out

def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    
    >>> parse(['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')'])
    ['+', 2, ['-', 5, 3], 7, 8]
    >>> parse(tokenize("(:= circle-area (function (r) (* 3.14 (* r r))))"))
    [':=', 'circle-area', ['function', ['r'], ['*', 3.14, ['*', 'r', 'r']]]]
    >>> parse(['3.17'])
    3.17
    >>> parse(['var'])
    'var'
    """
    if tokens.count('(') != tokens.count(')'):  ## make sure that parentheses are in pairs
        raise SnekSyntaxError('parentheses are not in pairs')
    
    token = tokens[0]
    ## 1. single element
    if len(tokens) == 1:  
        ## negative
        negative = False
        if token[0] == '-':
            token = token[1:]
            negative = True
        ## int
        if token.isdigit():
            if negative:
                token = '-' + token
            return int(token)
        ## float
        elif token.count('.') == 1 and token.replace('.', '').isdigit():
            if negative:
                token = '-' + token
            return float(token)
        ## symbol
        else:
            if negative:
                token = '-' + token
            return token
    ## 2. expression
    elif token == '(':
        out = []
        i = 1
        while True:
            if tokens[i] == '(':
                j = right_par_index(tokens, i)
                out.append(parse(tokens[i: j+1]))
                i = j
            elif tokens[i] == ')':
                break
            else:
                out.append(parse(tokens[i: i+1]))
            i += 1
        ## 2.1. variable definition syntax
        if tokens[1] == ':=':  
            if (
                len(out) != 3
                or not out[1]
                or type(out[1]) != str and type(out[1]) != list
                or type(out[1]) == list and any(type(i) != str for i in out[1])
            ):
                raise SnekSyntaxError('wrong syntax for variable definition')
        ## 2.2. function definition syntax
        elif tokens[1] == 'function':  
            if len(out) != 3 or type(out[1]) != list or any(type(param) != str for param in out[1]):
                raise SnekSyntaxError('wrong syntax for function definition')
        ## 2.3. if syntax
        elif tokens[1] == 'if':
            if len(out) != 4:
                raise SnekSyntaxError('wrong syntax for conditional expression')
        return out
    else:
        raise SnekSyntaxError('first element wrong type')

## Helper
def right_par_index(tokens, left_par_index):  ## 
    """
    Given the tokens and the left parenthesis,
    find the index of the corresponding right parenthesis.

    >>> right_par_index(['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')'], 3)
    7
    """
    left_par_count = 1
    end_index = left_par_index + 1
    for char in tokens[left_par_index+1:]:
        if char == '(':
            left_par_count += 1
        if char == ')':
            left_par_count -= 1
        if left_par_count == 0:
            return end_index
        end_index += 1
    raise SnekSyntaxError('parentheses are not in pairs')


######################
# Built-in Functions #
######################

## Calculation
def product(args):
    """
    Given a list of numbers, return the product of all numbers
    """
    if len(args) == 0:
        return 1
    if type(args[0]) != int and type(args[0]) != float:
        raise SnekEvaluationError('Non-number to product')
    return args[0] * product(args[1:])

def division(args):
    """
    Given a list of numbers, return the result of successively dividing the first number by the remaining numbers.
    """
    if len(args) == 0:
        raise Exception('no element for division')
    if len(args) == 1:
        return 1/args[0]
    return args[0]/product(args[1:])

## Bool
def compare(arguments, operator):
    """
    Given a list of arguments and an operator,
    evaluate to true if all of its arguments are true to the operator in sequence.
    """
    args = arguments[0]
    env = arguments[1]
    if len(args) <= 1:
        raise SnekSyntaxError('at least 2 elements to be compared')
    for i in range(len(args) - 1):
        if not operator(evaluate(args[i], env), evaluate(args[i+1], env)):
            return '#f'
    return '#t'

def snek_and(arguments):
    """
    Evaluates to true if all of its arguments are true.
    """
    args = arguments[0]
    env = arguments[1]
    for arg in args:
        arg = evaluate(arg, env)
        if arg == '#f':
            return '#f'
        elif arg == '#t':
            continue
        else:
            raise SnekSyntaxError('bool operator can only evaluate bool value')
    return '#t'

def snek_or(arguments):
    """
    Evaluates to true if any of its arguments is true.
    """
    args = arguments[0]
    env = arguments[1]
    for arg in args:
        arg = evaluate(arg, env)
        if arg == '#t':
            return '#t'
        elif arg == '#f':
            continue
        else:
            raise SnekSyntaxError('bool operator can only evaluate bool value')
    return '#f'

def snek_not(arguments):
    """
    Evaluates to false if its argument is true and true if its argument is false.
    """
    arg = arguments[0]
    env = arguments[1]
    if len(arg) != 1:
        raise SnekSyntaxError('not operator syntax error')
    arg = evaluate(arg[0], env)
    if arg == '#t':
        return '#f'
    elif arg == '#f':
        return '#t'
    else:
        raise SnekSyntaxError('not operator syntax error')

## List Basics
def cons(args):
    """
    Given two elements, construct a Pair.
    """
    if len(args) != 2:
        raise SnekSyntaxError('should be 2 arguments')
    return Pair(args[0], args[1])

def car(arg):
    """
    Get the CAR attribute of a Pair.
    """
    if len(arg) != 1 or type(arg[0]) != Pair:
        raise SnekEvaluationError('parameter should be a Pair')
    return arg[0].car

def cdr(arg):
    """
    Get the CDR attribute of a Pair.
    """
    if len(arg) != 1 or type(arg[0]) != Pair:
        raise SnekEvaluationError('parameter should be a Pair')
    return arg[0].cdr

def make_list(args):
    """
    Given a list of elements and construct a linked list made of Pairs.
    """
    if not args:
        return 'nil'
    return Pair(args[0], make_list(args[1:]))

## List Advanced
def length(args):
    """
    Given a linked list, return the length of it.
    """
    if len(args) != 1 or type(args[0]) != Pair and args[0] != 'nil':
        raise SnekEvaluationError('parameter for length is not list')
    arg = args[0]
    if arg == 'nil':
        return 0
    else:
        return 1 + length([arg.cdr])

def elt_at_index(args):
    """
    Given a linked list and an index, return the value at the index.
    """
    if len(args) != 2 or type(args[0]) != Pair or type(args[1]) != int or args[1] < 0:
        raise SnekEvaluationError('wrong argument for elt-at-index')
    l = args[0]
    i = args[1]
    if i == 0:
        return l.car
    if type(l.cdr) != Pair:
        raise SnekEvaluationError('elt-at-index non-list argument')
    return elt_at_index([l.cdr, i-1])

def concat(args):
    """
    Given a list of linked lists, return a concatenated list.
    """
    ## helper
    def copy_list(current_pair, l):
        if l == 'nil':
            return current_pair
        elif type(l) == Pair:
            if l.cdr == 'nil':
                current_pair.cdr = Pair(l.car, l.cdr)
                return current_pair.cdr
            else:
                current_pair.cdr = Pair(l.car, 'nil')
                return copy_list(current_pair.cdr, l.cdr)
        else:
            raise SnekEvaluationError('concat non-list element')
    
    new_list = 'nil'
    for l in args:
        if l == 'nil':
            continue
        elif type(l) == Pair:
            if new_list == 'nil':
                new_list = Pair(l.car, 'nil')
                current_pair = copy_list(new_list, l.cdr)
            else:
                current_pair = copy_list(current_pair, l)
        else:
            raise SnekEvaluationError('concat non-list element')
    return new_list

def snek_map_filter(args, func_name):
    """
    Given a function and a linked list as arguments, and given a func_name of 'map' or 'filter', 
    'map' returns a new list containing the results of applying the given function to each element of the given list,
    'filter' returns a new list containing only the elements of the given list for which the given function returns true.
    """
    ## exception
    if (
        len(args) != 2
        or type(args[0]) != Function and args[0] not in snek_builtins.values()
        or type(args[0]) == Function and len(args[0].param) != 1
        or type(args[1]) != Pair and args[1] != 'nil'
    ):
        raise SnekEvaluationError('wrong arguments for map and filter')
    if args[1] == 'nil':
        return 'nil'
    ## aliases
    func = args[0]
    l = args[1]
    ## init
    new_pair = Pair('nil', 'nil')
    sub_l = l
    sub_pair = new_pair
    ## built-in function
    if func in snek_builtins.values():
        ## iteration
        while True:
            value = func([sub_l.car])
            if func_name == 'map':
                sub_pair.cdr = Pair(value, 'nil')
                sub_pair = sub_pair.cdr
            elif func_name == 'filter':
                if value == '#t':
                    sub_pair.cdr = Pair(sub_l.car, 'nil')
                    sub_pair = sub_pair.cdr
            if sub_l.cdr == 'nil':
                break
            sub_l = sub_l.cdr
    ## custom function
    else:
        ## aliases
        param = func.param[0]
        env = func.env
        code = func.code
        ## init
        new_env = Environment(env)
        ## iteration
        while True:
            new_env.add_var(param, sub_l.car)
            value = evaluate(code, new_env)
            if func_name == 'map':
                sub_pair.cdr = Pair(value, 'nil')
                sub_pair = sub_pair.cdr
            elif func_name == 'filter':
                if value == '#t':
                    sub_pair.cdr = Pair(sub_l.car, 'nil')
                    sub_pair = sub_pair.cdr
            if sub_l.cdr == 'nil':
                break
            sub_l = sub_l.cdr
    return new_pair.cdr

def snek_reduce(args):
    """
    Given a function, a list, and an initial value as inputs,
    returns its output by successively applying the given function to the elements in the list.
    """
    ## exception
    if (
        len(args) != 3 
        or type(args[0]) != Function and args[0] not in snek_builtins.values()
        or type(args[0]) == Function and len(args[0].param) != 2
        or type(args[1]) != Pair and args[1] != 'nil'
    ):
        print(len(args))
        print(args[0])
        print(type(args[1]))
        # , snek_builtins[args[0]], type(args[1]))
        raise SnekEvaluationError('wrong arguments for reduce')
    if args[1] == 'nil':
        return args[2]
    ## aliases
    func = args[0]
    l = args[1]
    initval = args[2]
    ## init
    sub_l = l
    ## built-in function
    if func in snek_builtins.values():
        ## init
        sub_l = l
        out = func([initval, sub_l.car])
        ## iteration
        while True:
            if sub_l.cdr == 'nil':
                break
            sub_l = sub_l.cdr
            out = func([out, sub_l.car])
    ## custom function
    else:
        ## aliases
        params = func.param
        env = func.env
        code = func.code
        ## init
        new_env = Environment(env)
        sub_l = l
        out = initval
        ## iteration
        while True:
            new_env.add_var(params[0], out)
            new_env.add_var(params[1], sub_l.car)
            out = evaluate(code, new_env)
            if sub_l.cdr == 'nil':
                break
            sub_l = sub_l.cdr
    return out

## Begin
def begin(args):
    """
    Returns its last argument.
    """
    return args[-1]

## Dictionaries of Built-in Functions
snek_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': product,
    '/': division,

    'cons': cons,
    'car': car,
    'cdr': cdr,
    'list': make_list,

    'length': length,
    'elt-at-index': elt_at_index,
    'concat': concat,

    'map': lambda args: snek_map_filter(args, 'map'),
    'filter': lambda args: snek_map_filter(args, 'filter'),
    'reduce': snek_reduce,

    'begin': begin
}

snek_builtin_bools = {
    '=?': lambda args: compare(args, op.eq),
    '>': lambda args: compare(args, op.gt),
    '>=': lambda args: compare(args, op.ge),
    '<': lambda args: compare(args, op.lt),
    '<=': lambda args: compare(args, op.le),
    'and': snek_and,
    'or': snek_or,
    'not': snek_not
}


##############
# Evaluation #
##############

def evaluate(tree, env=None):
    """
    Evaluate the given syntax tree according to the rules of the Snek
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    >>> evaluate(3.14)
    3.14
    >>> evaluate(['+', 3, 7, 2])
    12
    >>> evaluate(['+', 3, ['-', 7, 5]])
    5
    """
    if env == None:  ## create new environment
        env = Environment(builtin)

    ## 1. single element function/variable
    if type(tree) == str:
        if tree == '#t' or tree == '#f' or tree == 'nil':
            return tree
        var = search_value(tree, env)
        if var in snek_builtins:
            return snek_builtins[var]
        elif var in snek_builtin_bools:
            return snek_builtin_bools[var]
        else:
            return var
    ## 2. single element number
    elif type(tree) == int or type(tree) == float:
        return tree
    ## 3. expression
    elif type(tree) == list:
        if tree == []:
            raise SnekEvaluationError
        func_sym = tree[0]
        ## 3.1. Special Form
        ## 3.1.1. variable definition
        if func_sym == ':=':
            if type(tree[1]) == list:  ## easier function definition
                name = tree[1][0]
                value = Function(env, tree[1][1:], tree[2])
            else:
                name = tree[1]
                if type(tree[2]) == str and tree[2] in snek_builtins:
                    value = tree[2]
                else:
                    value = evaluate(tree[2], env)
            env.add_var(name, value)
            return value
        ## 3.1.2. function definition
        elif func_sym == 'function':
            return Function(env, tree[1], tree[2])
        ## 3.1.3. conditional expression
        elif func_sym == 'if':
            if evaluate(tree[1], env) == '#t':
                return evaluate(tree[2], env)
            elif evaluate(tree[1], env) == '#f':
                return evaluate(tree[3], env)
            else:
                raise SnekEvaluationError('condition evaluation should be bool value')
        ## 3.1.4. del
        elif func_sym == 'del':
            if len(tree) != 2 or type(tree[1]) != str:
                raise SnekSyntaxError('del syntax error')
            var = tree[1]
            if var in env.vars:
                out = env.vars[var]
                del env.vars[var]
                return out
            else:
                raise SnekNameError('variable name not defined locally')
        ## 3.1.5. let
        elif func_sym == 'let':
            if len(tree) != 3 :
                raise SnekSyntaxError('let syntax error')
            new_env = Environment(env)
            for binding in tree[1]:
                if len(binding) != 2:
                    raise SnekSyntaxError('let syntax error')
                value = evaluate(binding[1], env)
                new_env.add_var(binding[0], value)
            return evaluate(tree[2], new_env)
        ## 3.1.6. set!
        elif func_sym == 'set!':
            if len(tree) != 3 or type(tree[1]) != str:
                raise SnekSyntaxError('set! syntax error')
            var = tree[1]
            value = evaluate(tree[2], env)
            current_env = env
            while True:
                if var in current_env.vars:
                    current_env.vars[var] = value
                    break
                if current_env.parent == None:
                    raise SnekNameError
                current_env = current_env.parent
            return value
        ## 3.2. call function
        else:
            if type(func_sym) == list:
                func = evaluate(func_sym, env)
            else:
                func = search_value(func_sym, env)
            ## 3.4.1. bools
            if func in snek_builtin_bools:
                args = [[tree[i] for i in range(1, len(tree))], env]
                return snek_builtin_bools[func](args)
            args = [evaluate(tree[i], env) for i in range(1, len(tree))]
            ## 3.4.2. built-in functions
            if func in snek_builtins:
                return snek_builtins[func](args)
            ## 3.4.3. custom functions
            if type(func) == Function:
                new_env = Environment(func.env)
                if len(args) != len(func.param):
                    raise SnekEvaluationError('wrong arguments number')
                for i in range(len(args)):
                    new_env.add_var(func.param[i], args[i])
                return evaluate(func.code, new_env)
            raise SnekEvaluationError('first element should be a valid function')
    else:
        raise SnekSyntaxError('cannot evaluate this type of expression')

## Helper
def search_value(var, environemnt):
    """
    Given a variable and the current environment,
    find the variable in it and in its parent,
    return the value
    """
    if type(var) != str:
        raise SnekEvaluationError('wrong variable type')
    if var in environemnt.vars:
        return environemnt.vars[var]
    if environemnt.parent == None:
        raise SnekNameError('variable is not defined')
    return search_value(var, environemnt.parent)

def result_and_env(tree, env=None):
    """
    a function for test
    """
    if env == None:  ## create new environment
        env = Environment(builtin)
    return (evaluate(tree, env), env)


###############
# Environment #
###############

class Environment():
    """
    Environment class
    Attributes:
        parent: parent environment
        vars: a dictionary of varialbe names to their values
    Methods:
        add_var: add variable to self.vars
    """
    def __init__(self, parent):
        if parent != None:
            assert type(parent) == Environment
        self.parent = parent
        self.vars = {}
    
    def add_var(self, name, value):
        self.vars[name] = value

## Built-in Environment
builtin = Environment(None)
for key in snek_builtins:
    builtin.vars[key] = key
for key in snek_builtin_bools:
    builtin.vars[key] = key


############
# Function #
############

class Function():
    """
    Function class
    Attributes:
        env: parent environment
        param (list): parameters
        code (list): function code in the form of a parsed list
    """
    def __init__(self, environment, parameters, code):
        self.env = environment
        self.param = parameters
        self.code = code


########
# List #
########

class Pair():
    """
    Pair class for cons cells
    Attributes:
        car: Contents of the Address Register
        cdr: Contents of the Decrement Register
    """
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr


##############################
# File / REPL / Command Line #
##############################

def evaluate_file(file, env=None):
    """
    Evaluates code in a file.
    """
    with open(file) as f:
        source = f.read()
    return evaluate(parse(tokenize(source)), env)

def REPL():
    """
    Read, Evaluate, Print Loop
    """
    environment = Environment(builtin)
    ## command line arguments
    for file_name in sys.argv[1:]:
        if file_name[-5:] == '.snek':
            evaluate_file(file_name, environment)
    ## REPL
    while True:
        inp = input('in> ')
        if inp == 'QUIT':
            break
        try:
            outp = evaluate(parse(tokenize(inp)), environment)
        except Exception as err:
            print('Exception:', err)
        else:
            print('out> ', outp)


########
# Main #
########

if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    REPL()

    pass

