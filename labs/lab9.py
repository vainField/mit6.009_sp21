#!/usr/bin/env python3
"""6.009 Lab 9: Snek Interpreter"""

import doctest
# NO ADDITIONAL IMPORTS!


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
    ## single element
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
    ## expression
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
        if tokens[1] == ':=':  ## variable definition syntax
            if (
                len(out) != 3
                or not out[1]
                or type(out[1]) != str and type(out[1]) != list
                or type(out[1]) == list and any(type(i) != str for i in out[1])
            ):
                raise SnekSyntaxError('wrong syntax for variable definition')
        elif tokens[1] == 'function':  ## function definition syntax
            if len(out) != 3 or type(out[1]) != list or any(type(param) != str for param in out[1]):
                raise SnekSyntaxError('wrong syntax for function definition')
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

## Functions
def product(list):
    if len(list) == 0:
        return 1
    return list[0] * product(list[1:])

def division(list):
    if len(list) == 0:
        raise Exception('no element for division')
    if len(list) == 1:
        return 1/list[0]
    return list[0]/product(list[1:])

## Dictionary
snek_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': product,
    '/': division
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
        var = search_value(tree, env)
        if var in snek_builtins:
            return snek_builtins[var]
        else:
            return var
    ## 2. single element number
    elif type(tree) == int or type(tree) == float:  
        return tree
    ## 3. expression
    elif type(tree) == list:  
        func_sym = tree[0]
        ## 3.1. variable definition
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
        ## 3.2. function definition
        elif func_sym == 'function':  
            return Function(env, tree[1], tree[2])
        ## 3.3. call function
        else:  
            if type(func_sym) == list:
                func = evaluate(func_sym, env)
            else:
                func = search_value(func_sym, env)
            args = [evaluate(tree[i], env) for i in range(1, len(tree))]
            if func in snek_builtins:
                return snek_builtins[func](args)
            elif type(func) == Function:
                new_env = Environment(func.env)
                if len(args) != len(func.param):
                    raise SnekEvaluationError('wrong arguments number')
                for i in range(len(args)):
                    new_env.add_var(func.param[i], args[i])
                return evaluate(func.code, new_env)
            else:
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
# REPL #
########

def REPL():
    """
    Read, Evaluate, Print Loop
    """
    environment = Environment(builtin)
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
# MAIN #
########

if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    REPL()

    # print(
    #     tokenize("(:= square (function (x) (* x x)))"), '\n',
    #     parse(['(', ':=', 'square', '(', 'function', '(', 'x', ')', '(', '*', 'x', 'x', ')', ')', ')'] ), '\n',
    #     evaluate([':=', 'square', ['function', ['x'], ['*', 'x', 'x']]])
    # )

    # evaluate(parse(tokenize("")))
    # env = Environment(builtin)
    # evaluate(parse(tokenize("(:= square (function (x) (* x x)))")), env)
    # evaluate(parse(tokenize("(square 2)")), env)

    pass
