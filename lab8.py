import doctest
from typing import SupportsBytes
from instrument import instrument

# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.

class Symbol:
    """
    ## Using Python Operators with Symbolic Expressions
    >>> Var('a') * Var('b')
    Mul(Var('a'), Var('b'))
    >>> 2 + Var('x')
    Add(Num(2), Var('x'))
    >>> Num(3) / 2
    Div(Num(3), Num(2))
    >>> Num(3) + 'x'
    Add(Num(3), Var('x'))

    ## Derivatives
    >>> x = Var('x')
    >>> y = Var('y')
    >>> z = 2*x - x*y + 3*y
    >>> print(z.deriv('x'))  # unsimplified, but the following gives us (2 - y)
    2 * 1 + x * 0 - (x * 0 + y * 1) + 3 * 0 + y * 0
    >>> print(z.deriv('y'))  # unsimplified, but the following gives us (-x + 3)
    2 * 0 + x * 0 - (x * 1 + y * 0) + 3 * 1 + y * 0

    ## Evaluation
    >>> z = Add(Var('x'), Sub(Var('y'), Mul(Var('z'), Num(2))))
    >>> z.eval({'x': 7, 'y': 3, 'z': 9})
    -8
    >>> z.eval({'x': 3, 'y': 10, 'z': 2})
    9
    """
    ## Symbolic Rank for Adding Parenthesis
    def rank(self):
        if isinstance(self, Add):
            return 'a'
        if isinstance(self, Sub):
            return 'b'
        if isinstance(self, Mul):
            return 'ba'
        if isinstance(self, Div):
            return 'bb'
        else:
            return 'bba'

    def __gt__(self, other):
        return len(self.rank()) > len(other.rank())
    
    def __ge__(self, other):
        if isinstance(self, Sub) and isinstance(other, Sub):
            return True
        if isinstance(self, Div) and isinstance(other, Div):
            return True
        else:
            return self.rank() > other.rank()


    ## Using Python Operators with Symbolic Expressions
    def __add__(self, other):
        return Add(self, other)
    
    def __radd__(self, other):
        return Add(other, self)

    def __sub__(self, other):
        return Sub(self, other)
    
    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        return Mul(self, other)
    
    def __rmul__(self, other):
        return Mul(other, self)

    def __truediv__(self, other):
        return Div(self, other)

    def __rtruediv__(self, other):
        return Div(other, self)
    

    ## Simplification
    def simplify(self):
        """
        >>> x = Var('x')
        >>> y = Var('y')
        >>> z = 2*x - x*y + 3*y
        >>> print(z.simplify())
        2 * x - x * y + 3 * y
        >>> print(z.deriv('x'))
        2 * 1 + x * 0 - (x * 0 + y * 1) + 3 * 0 + y * 0
        >>> print(z.deriv('x').simplify())
        2 - y
        >>> print(z.deriv('y'))
        2 * 0 + x * 0 - (x * 1 + y * 0) + 3 * 1 + y * 0
        >>> print(z.deriv('y').simplify())
        0 - x + 3
        >>> Add(Add(Num(2), Num(-2)), Add(Var('x'), Num(0))).simplify()
        Var('x')
        """
        if isinstance(self, Var) or isinstance(self, Num):   ## single character or number
            return self
        else:
            left = self.left.simplify()
            right = self.right.simplify()

            if isinstance(left, Num) and isinstance(right, Num):   ## both operands are numbers
                return Num(type(self)(left, right).eval({}))

            if isinstance(self, Add):   ## one operand is 0
                if left.n == 0:
                    return right
                if right.n == 0:
                    return left
                return Add(left, right)
            if isinstance(self, Sub):   ## subtrahend is 0
                if right.n == 0:
                    return left
                return Sub(left, right)
            if isinstance(self, Mul):   ## one operand is 0 or 1
                if left.n == 0 or right.n == 0:
                    return Num(0)
                if left.n == 1:
                    return right
                if right.n == 1:
                    return left
                return Mul(left, right)
            if isinstance(self, Div):   ## divisor is 1 or dividend is 0
                if right.n == 1:
                    return left
                if left.n == 0:
                    return Num(0)
                return Div(left, right)


class Var(Symbol):
    n = None
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'

    def deriv(self, var):
        if str(self) == var:
            return Num(1)
        else:
            return Num(0)
    
    def eval(self, mapping):
        if str(self) in mapping:
            return mapping[str(self)]
        else:
            return self


class Num(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Num(' + repr(self.n) + ')'

    def __eq__(self, other):
        return self.n == other.n

    def deriv(self, var):
        return Num(0)

    def eval(self, mapping):
        return self.n


class BinOp(Symbol):
    """
    >>> z = Add(Var('x'), Sub(Var('y'), Num(2)))
    >>> repr(z)  # notice that this result, if fed back into Python, produces an equivalent object.
    "Add(Var('x'), Sub(Var('y'), Num(2)))"
    >>> str(z)  # this result cannot necessarily be fed back into Python, but it looks nicer.
    'x + y - 2'

    >>> z = Mul(Var('x'), Add(Var('y'), Var('z')))
    >>> str(z)
    'x * (y + z)'
    """
    n = None
    def __init__(self, left, right):
        if type(left) == int:
            left = Num(left)
        if type(right) == int:
            right = Num(right)
        if type(left) == str and len(left) == 1:
            left = Var(left)
        if type(right) == str and len(right) == 1:
            right = Var(right)
        if not isinstance(left, Symbol) or not isinstance(right, Symbol):
            raise TypeError('parameters should be Symbol')
    
        self.left = left
        self.right = right
    
    def __str__(self):
        result_left = str(self.left)
        result_right = str(self.right)
        if self > self.left:
            result_left = '(' + result_left + ')'
        if self >= self.right:
            result_right = '(' + result_right + ')'
        return result_left + self.op_str() + result_right

    def __repr__(self):
        return self.op_repr() + '(' + repr(self.left) + ', ' + repr(self.right) + ')'


class Add(BinOp):
    def op_str(self):
        return ' + '

    def op_repr(self):
        return 'Add'

    def deriv(self, var):
        return Add(self.left.deriv(var), self.right.deriv(var))
    
    def eval(self, mapping):
        return self.left.eval(mapping) + self.right.eval(mapping)

class Sub(BinOp):
    def op_str(self):
        return ' - '

    def op_repr(self):
        return 'Sub'

    def deriv(self, var):
        return Sub(self.left.deriv(var), self.right.deriv(var))

    def eval(self, mapping):
        return self.left.eval(mapping) - self.right.eval(mapping)

class Mul(BinOp):
    def op_str(self):
        return ' * '

    def op_repr(self):
        return 'Mul'

    def deriv(self, var):
        return Add(Mul(self.left, self.right.deriv(var)), Mul(self.right, self.left.deriv(var)))

    def eval(self, mapping):
        return self.left.eval(mapping) * self.right.eval(mapping)

class Div(BinOp):
    def op_str(self):
        return ' / '

    def op_repr(self):
        return 'Div'

    def deriv(self, var):
        return Div(
            Sub(Mul(self.right, self.left.deriv(var)), Mul(self.left, self.right.deriv(var))),
            Mul(self.right, self.right)
        )

    def eval(self, mapping):
        return self.left.eval(mapping) / self.right.eval(mapping)


## Parsing Symbolic Expressions
def sym(string):
    return parse(tokenize(string))

# helper functions / variables
characters = 'abcdefghijklmnopqrstuvwxyz' + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
integers = '0123456789'
operators = '+-*/'
parenthesis = '()'

def tokenize(string):
    """
    >>> tokenize("(x * (2 + 3))")
    ['(', 'x', '*', '(', '2', '+', '3', ')', ')']
    >>> tokenize("(x * (-23 + 3))")
    ['(', 'x', '*', '(', '-23', '+', '3', ')', ')']
    >>> tokenize('x')
    ['x']
    >>> tokenize('20')
    ['20']
    >>> tokenize('(y * -2)')
    ['(', 'y', '*', '-2', ')']
    """
    string = ' ' + string + ' '   ## help to recognize continuouse numbers
    result = []
    number = ''

    for i in range(1, len(string)-1):
        if string[i] != ' ':
            if (
                (string[i+1] in integers or string[i-1] in integers or string[i-1] == '-') and 
                (string[i] in integers or string[i] == '-')
            ):   ## continuous number
                number += string[i]
            elif number:   ## continuouse number ends
                result.append(number)
                number = ''
                if string[i] in parenthesis or string[i] in operators:
                    result.append(string[i])
            else:
                result.append(string[i])
        if i == len(string)-2 and number:   ## string ends with a continuous number
            result.append(number)
    return result

def parse(tokens):
    """
    >>> tokens = tokenize("(x * (2 + 3))")
    >>> parse(tokens)
    Mul(Var('x'), Add(Num(2), Num(3)))
    >>> tokens = tokenize("((2 + 3) * x)")
    >>> parse(tokens)
    Mul(Add(Num(2), Num(3)), Var('x'))
    """
    if len(tokens) == 0 or tokens[0] in operators:
        raise TypeError('wrong type of tokens')

    token = tokens[0]
    if token in integers or len(token) > 1:   ## Num
        return Num(int(token))
    if token in characters:   ## Var
        return Var(token)

    ## BinOp
    left_parenthesis = 0
    i = 1
    for t in tokens[1:]:
        if t == '(':
            left_parenthesis += 1
        if t == ')':
            left_parenthesis -= 1
        if left_parenthesis == 0:
            break
        i += 1
    operator = tokens[i+1]
    Op = Add if operator == '+' else Sub if operator == '-' else Mul if operator == '*' else Div
    return Op(parse(tokens[1: i+1]), parse(tokens[i+2: -1]))


if __name__ == '__main__':
    doctest.testmod()