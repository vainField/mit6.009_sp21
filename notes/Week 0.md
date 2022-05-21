# <u>L0. Intro</u>

**Programming:** analyzing problems, developing plans

**Coding:** translating plans into Python

**Debugging:** developing test cases, verifying correctness, finding and fixing errors

## Deliberate Practice

1. watch how experienced programmers approach problems
2. program!
3. receive feedback from more experienced programmers

- *Lectures/recitations* equip you with tools useful for attacking those problems.
  - Take notes in your own words and review them later
  - Ask questions! We want to have a conversation.
- *Labs* give opportunities to practice new techniques/skills to solve interesting problems.
  - **Formulate a plan before writing code**
    - Try to understand the problem thoroughly before writing code
    - When things go wrong, step away from the code and revisit the plan
- *Checkoffs and office hours* give opportunities to receive expert feedback.

## Growth, not Perfection

<img src="image.assets/Screen Shot 2021-04-21 at 21.01.54.png" alt="Screen Shot 2021-04-21 at 21.01.54" style="zoom:33%;" />

This Week: Python Mental Model

## *Thinking*

Lecture 0 通过刻意练习的概念介绍了这个课程的主要内容和架构。刻意练习是在很多领域成为专家的有效方法，向有经验的人学习，动手练习，有经验的人的反馈，这三者缺一不可。那么对于自学者来说，第三项便是最欠缺的。

# <u>R0. Python Notional Machine</u>

## Variables and data types

### Mutability

Unlike integers, lists are mutable:

```python
y = ['baz', 302, 303, 304]
x = y
x[0] = 388 
print('y:', y)
```

```python
y:[388,302,303,304]
```

As seen above, we have to be careful about sharing (also known as "aliasing") mutable data!

```python
a = [301, 302, 303] 
b = [a, a, a] 
b[0][0] = 304 
print(b) 
print(a)

```

```python
[[304, 302, 303], [304, 302, 303], [304, 302, 303]]
[304, 302, 303]
```

#### Tuples

Tuples are a lot like lists, except that they are immutable.

Unlike a list, we can't change the top most structure of a tuple.

```python
x = ('baz', [301, 302], 303, 304) 
y = x
x[0] = 388
```

```python
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-11-8a08f6fbfa16> in <module>
----> 1 x[0] = 388
TypeError: 'tuple' object does not support item assignment
```

but it might have members that are themselves mutable.

```python
x[1][0] = 311 
print('x:', x, '\ny:', y)
```

```python
x: ('baz', [311, 302], 303, 304)
y: ('baz', [311, 302], 303, 304)
```

#### Strings

Strings are also immutable. We can't change them once created.

#### Back to lists: append, extend, and the '+' and '+=' operators

##### Append

```python
x = [1, 2, 3]
y = [4, 5]
x.append(y)
y[0] = 99
print('x:', x, '\ny:', y)
```

```python
x: [1, 2, 3, [99, 5]]
y: [99, 5]
```

##### Extend

```python
x = [1, 2, 3]
y = [4, 5]
x.extend(y)
y[0] = 88
print('x:', x, '\ny:', y)
```

```python
x: [1, 2, 3, 4, 5]
y: [88, 5]
```

##### +

```python
x = [1, 2, 3] 
y = x
x = x + [4, 5] 
print('x:', x, '\ny:', y)
```

```python
x: [1, 2, 3, 4, 5]
y: [1, 2, 3]
```

##### +=

```python
x = [1, 2, 3]
y = x
x += [4, 5]
y[0] = 77
print('x:', x, '\ny:', y)
```

```python
x: [77, 2, 3, 4, 5]
y: [77, 2, 3, 4, 5]
```

**So x += <something> is NOT the same thing as x = x + <something> if x is a list!**

## Functions and scoping

```python
x = 500 
def foo(y):
	return x + y 
z = foo(307)
def bar(x): 
	x = 1000
	return foo(307) 
w = bar('hi')
print('x:', x, '\nw:', w)
```

```python
x: 500 
w: 807
```

Importantly, foo "remembers" that it was created in the global environment, so looks in the global environment to find a value for x . It does **not** look back in its "call chain".

### Optional arguments and default values

```python
def foo(x, y = []): 
	y = y + [x]
	return y
a = foo(7)
b = foo(8, [1, 2, 3])
c = foo(7)
print('a:', a, '\nb:', b, '\nc:', c)
```

```python
a: [7]
b: [1, 2, 3, 8]
c: [7]
```



```python
def foo(x, y = []):
	y.append(x) # different here 
	return y
a = foo(7)
b = foo(8, [1, 2, 3]) 
print('a:', a, '\nb:', b)
```

```python
a: [7]
b: [1, 2, 3, 8]
```

```python
c = foo(7)
print('a:', a, '\nb:', b, '\nc:', c)
```

```python
a: [7, 7]
b: [1, 2, 3, 8]
c: [7, 7]
```

The default value to an optional argument is only evaluated once, at function *definition* time. The moral here is to be **very** careful (and indeed it may be best to simply avoid) having optional/default arguments that are mutable structures like lists.

## Reference Counting

```python
import sys
L1 = [301, 302, 303] 
print(sys.getrefcount(L1)) 
L2 = L1 
print(sys.getrefcount(L1)) 
L3 = [L1, L1, L1] 
print(sys.getrefcount(L1)) 
L3.pop() 
print(sys.getrefcount(L1)) 
L3 = 307 
print(sys.getrefcount(L1))
```

```python
2 
3 
6 
5 
3
```

Python knows to throw away an object when its "reference counter" reaches zero.

## *Thinking*

1. Recitation 0 复习了Python的一些基础知识：变量，数据类型，函数，环境。主要讨论了两个极易出现bug的问题，可变性和作用域（scoping）。
2. 可变性（mutability）关系到变量在内存中的状态，可变数据类型的不慎使用可能会导致对于变量的意外改变。但显然它也是很多算法技巧的基础。
3. 作用域（scoping）和函数定义的环境有关，由此影响到变量所能影响到的范围。同样，恰当的使用也是一些算法技巧的基础。
4. 另外还讨论了一个细节问题，即函数的可选参数及其默认值。如果可选参数为可变数据类型，其默认值在内存中的位置在函数定义时即被确定并不再改变。因此如果函数的定义中有任何对于可选参数默认值的操作，被改变的默认值即会影响到下一次的函数调用（如果调用默认值）。

# <u>Lab0.0. Basics</u>

## The Command Line

A *command line* is a text-based interface to your computer.

### Commands

- the name of the program we want to run,
- zero or more "options" that change the behavior of the program, and
- zero or more "arguments" on which the program should operate.

`pwd`: **p**rint **w**orking **d**irectory

`ls`: list of the files and folders contained within the current directory

### Notation

```
$ pwd
$ ls
```

the dollar sign represents the prompt, so you should not type the dollar sign itself into your terminal

### Arguments

Options generally start with a hyphen `-`, and they modify the behavior of a program.

```nohighlight
$ ls -l
```

### Navigating with cd

`cd`: **c**hange **d**irectory

`cd ..`: move back up the directory hierarchy

`cd Downloads/Music`

`cd ../..`

If you ever get lost in your filesystem, you can also just run `cd` with no arguments to return to your "home" directory

### Quick Overview of Commands Related to Navigation

`ls` ("list")

The `-l` option causes `ls` to print more information (a "long" listing) for each file. The `-a` option ("all") causes `ls` to show hidden files (files or directories whose names begin with a period `.`, which are normally not shown).

`mv` ("move")

Moves or renames a file. Typical usage involves two arguments, a source (the file to be moved) and a destination (either a new name for the file, or a directory into which the file should be moved).

`rm` ("remove")

Deletes a file given as an argument.

`mkdir` ("make directory")

Creates a new directory. For example, to create a directory called `hello` in the current working directory, run `mkdir hello`.

### Running Python

```nohighlight
$ python lab.py
```

```nohighlight
$ python -i lab.py
```

Specifying the `-i` flag will cause Python not to exit after evaluating the code in the given file, but rather to enter into a "REPL" (**R**ead-**E**valuate-**P**rint-**L**oop)

### Installing Python Packages with Pip

```nohighlight
$ pip install pytest
```

### Running Pytest

We will be using `pytest` as a means of testing the behaviors you implement in your `lab.py` files for correctness.

`import pytest` in python

- `pytest -v test.py` will display more information about the test cases as they are being run.
- `pytest -x test.py` will cause execution to stop after the first failed test case (if any), rather than running all test cases
- `pytest -s test.py` will cause print statements to print to the terminal immediately as test cases are run (without `-s`, the output from print statements is collected and only displayed after running all test cases)
- `pytest -k PATTERN test.py` will run only the test cases that contain `PATTERN` in their name. For example, in lab 0, running `pytest -k echo test.py` will cause only the test cases with "echo" in their name to run (in this case, running only the tests corresponding to that portion of the lab).

### Other Tips

- Pro-tip: "Tab Completion"
  - `cd Dow` $\to$ `cd Downloads`

- Pro-tip: Up-arrow and Down-arrow for Navigating History

- Avoid putting spaces in filenames
  - `cd "My Documents"` or `cd My\ Documents`

## Designing Programs

### A General Framework for Program Design

**avoid the temptation to write code until you have a plan in mind**

George Polya, *How To Solve It* (Princeton University Press, 1945), some regard as the best book ever written about teaching and problem solving

1. **Understand the Problem**
   1. What problem are you trying to solve?
   2. What is the ***input***, and what is the ***output***? How can we ***represent*** these in Python?
   3. What are some example input/output relationships? Come up with a few small, specific examples you can use to test later.
      1. How do you, a human, solve those simple cases? Do those steps generalize? How can we break that down into steps small enough for the computer to understand?
2. **Make A Plan**
   1. Look for the connection between the input and the output. What are the high-level operations that need to be performed to produce the output? How can you construct the output using those operations? How can you test the operations?
   2. What information, beyond the inputs, will you need to keep track of? What types of Python objects are useful ways to represent that information?
   3. Have you read or written a related program before? If so, pieces of that solution might be helpful here.
   4. Can you break the problem down into simpler cases? If you can't immediately solve the proposed problem, try first solving a subpart of the problem, or a related but simpler problem (sometimes, a more general or more specific case).
   5. Does your plan make use of all the inputs? Does it produce all the proper outputs?
   6. Thinking back to your understanding of the problem, are there any interesting "edge cases" that should be considered? Does your plan account for those?
3. **Implement the Plan**
   1. You may be able to implement several of the important high-level operations as individual "helper" functions.
   2. As you are going, consider the style guidelines outlined [here](https://py.mit.edu/spring21/notes/style). If you find yourself repeating a computation, you may want to reorganize now (rather than at the end).
   3. As you are going, check each step and each helper function:
      1. Can you clearly see that the step is correct in a general sense?
      2. Can you prove that it is correct in a general sense?
      3. Does the step pass your test cases from earlier?
      4. How can you use that result as part of the larger program?
4. **Look Back**
   1. Test both for correctness and style.
   2. For each of the test cases you constructed earlier, run it and make sure you see the result you expect. Are there other test cases you should consider?
   3. Could you have solved the problem a different way? If so, what are the benefits and drawbacks of the solution you chose?
   4. Can you use the result for some other problem? Can you use similar programming structures for some other problem?
   5. Look for opportunities to improve the style of your code according to the rules discussed in the previous section.
      1. Are the names of your functions and variables concise and descriptive?
      2. Are you repeating a computation anywhere?
      3. Are there functions or other pieces of your code that could be generalized?

### Organizing the Design Process

1. ***Sketch out a high-level outline on paper***, in any format that is helpful to you. This can involve *working through specific cases by hand*, *outlining useful helper functions*, *drawing diagrams*, writing "pseudocode", or anything else that is helpful to you.
2. ***Explicitly write an outline using comments***. Particularly *once the high-level design starts to take shape a bit*, it can be helpful to organize your thoughts using comments in an actual Python file, even before writing any actual code.

## Style

### Introduction

We'll be concerned with style from a higher-level perspective that focuses on how your code is *structured*, rather than how it is *formatted*.

- **Don't Repeat Yourself (DRY)**: Avoid multiple fragments of code that describe redundant logic.
- **Names Matter**: Choose concise, descriptive names for functions, parameters, and other variables.
- **Documentation Matters**: Use docstrings and comments to describe assumptions and document non-obvious features of the code.
- **Generality Wins**: Define logic, functions, and programs as generally as possible.
- **Plan for Change**: Where possible, make programs that are (relatively) easy to change, should the need arise.

Following these guidelines will help you to:

- improve the readability of your code (other people *will* read your code, even if those other people are all either 6.009 staff or future versions of yourself)
- reduce the number of errors in your code, and make it easier to spot/fix them
- make it easier to make changes to your program if you need to
- minimize the amount of code you write (the less code we have, the fewer opportunities there are for bugs!)

### Don't Repeat Yourself

If you have identical code (or very similar code) in multiple places in your program, then noticing an error (or some other opportunity for improvement) in one copy requires making appropriate changes to *all* copies.

#### The Rule of Three

If a piece of code or a computation is repeated *three* or more times, abstract that computation into a function, a loop or a variable.

A better approach for larger chunks might be the rule of *two*.

#### Boolean Laundering

```python
def is_negative(x):
    if (x < 0) == True:
        return True
    else:
        return False
```

```python
    if x < 0:
        return True
```

```python
def is_negative(x):
    return x < 0
```

### Names Matter

Variable names should describe what they represent (not just their types!). Single letter names are okay in some situations, but use such names sparingly.

#### Concise, Descriptive Names

It is also generally a good idea to avoid abbreviations, since, while their meanings may be evident to you, they may not be to someone else.

```python
def circle_circumference(radius):
     return 2 * PI * radius

def circle_area(radius):
    return PI * radius**2

def sphere_surface_area(radius):
    return 4 * circle_area(radius)

def sphere_volume(radius):
    return 4/3 * PI * radius**3
```

While it can be tempting to use generic one-character names for any looping variables, it is often possible to clarify things by using more descriptive names.

```python
def longest_word_in_file(fname):
    longest = 0
    with open(fname) as f:
        for line in f:
            for word in line.split():
                if len(word) > longest:
                    longest = len(word)
    return longest
```

#### Magic Numbers

```python
MASSACHUSETTS_TAX_RATE = 1.0625

def total_cost(raw_cost):
    return raw_cost * MASSACHUSETTS_TAX_RATE # instead of 1.0625
```

#### One Purpose For Each Variable

As a rule of thumb, don't reuse parameters, and don't reuse variable names.

### Documentation Matters

The kindest thing you can do for future people reading your code (which includes not only your 6.009 staff, but also **your future self!**) is to document your code, and to do so judiciously.

#### Docstrings

One important kind of documentation is a [docstring](https://www.python.org/dev/peps/pep-0257/), which is a regular Python string on the first line of a function, and which serves as documentation for that function.

- a brief one-sentence description of the function's behavior
- if necessary, a longer description of the behavior
- a description of inputs (including types as well as any other expectations about those values)
- a description of effects (including return value/type, any exceptions that might be raised, or other side effects of the function.

#### Comments

As you are writing code, you should document the pieces of the code that are non-obvious, but let the code speak for itself where it can.

```python
velocity = 5  # meters / second

sum = n*(n+1)/2  # Gauss's formula for the sum of 1...n

# here we're using the approximation that sin(x) ~= x when x is small
moon_diameter_meters = moon_distance_meters * apparent_angle_radians
```

Good variable names can reduce the need for certain kinds of comments. 

```python
n = 60*60*24  # number of seconds in a day
seconds_per_day = 60*60*24
```

#### Commented-out Code

When your code is ready, you should remove sections of unused code that have been commented out.

### Generality Wins

For example, the `square` function is not defined in the `math` module, nor is `cube`. This is because they are both specific cases for the `pow` function (exponentiation), which *is* in the `math` module.

#### Avoid Superfluous Special Cases

```python
def sum_all(values):
    if len(values) == 0:
        return 0
    elif len(values) == 1:	# unnecessary
        return values[0]
    else:
        return values[0] + sum_all(values[1:])
```

#### Special Cases for the Sake of Efficiency

To quote [Donald Knuth](https://en.wikipedia.org/wiki/Donald_Knuth):

> "We should forget about small efficiencies, say about 97% of the time: premature optimization is the root of all evil. Yet we should not pass up our opportunities in that critical 3%"

### Plan for Change

Oftentimes, when writing programs, you may find that *the requirements for the program you're writing may change* (or you may find that the problem you *actually* wanted to solve isn't the one solved by the program you're writing).

#### Avoid Monolithic Functions

It can be tempting, when writing a complicated program, to implement the entire program in a single function. Howerve, it is a good idea to try to separate logically-independent suboperations from each other.

#### Store Local Information Locally

It is a good idea to avoid using global variables altogether. [This page](http://wiki.c2.com/?GlobalVariablesAreBad) has some good examples of the dangers of global variables.

If you want a single function to have access to the same piece of data across multiple calls to that function, you could consider *using a closure*. If you want multiple functions to have access to the same piece of data, you could consider *creating a class*.

#### Return Results, Don't Print Them

In general, only the highest-level parts of a program should interact with the human user or the console. Lower-level parts should take their input as parameters and return their output as results.

# <u>Lab0. Audio Processing</u>

## Representing Sound

In physics, when we talk about a sound, we are talking about waves of air pressure.

When we use a microphone to capture a sound digitally, we do so by making periodic measurements of an electrical signal proportional to this air pressure.

When a speaker plays back that sound, it does so by converting these measurements back into waves of alternating air pressure (by moving a diaphragm proportionally to those captured measurements).

### Python Representation

Our Pythonic representation of a sound will consist of a dictionary with three key/value pairs, e.g.

```python
s = {
    'rate': 8000,
    'left' [0.00, 0.59, 0.95, 0.95, 0.59, 0.00, -0.59, -0.95, -0.95, -0.59],
    'right': [1.00, 0.91, 0.67, 0.31, -0.10, -0.50, -0.81, -0.98, -0.98, -0.81],
}
```

## Manipulations

### Backwards Audio

 e.g. a crash cymbal

### Mixing Audio

`mix` should take three inputs: two sounds (in our dictionary representation) and a "mixing parameter" $p$ (a `float` such that $0 \leq p \leq 1$).

### Echo

- `sound`: a dictionary representing the original sound
- `num_echos`: the number of additional copies of the sound to add
- `delay`: the amount (in **seconds**) by which each "echo" should be delayed
- `scale`: the amount by which each echo's samples should be scaled

### Pan

In particular, if our sound is $N$ samples long, then:

- We scale the first sample in the right channel by 0, the second by $\frac{1}{N-1}$, the third by $\frac{2}{N-1}, \ldots$ and the last by 1 .

- At the same time, we scale the first sample in the left channel by 1 , the second by $1-\frac{1}{N-1}$, the third by $1-\frac{2}{N-1}, \ldots$ and the last by 0 .

### Removing Vocals from Music

we compute `(left-right)`, i.e., the difference between the left and right channels at that point in time, and use that value as **both** the left and right values in the output at that time.

(Typically, many instruments are recorded so they they favor one side of the stereo track over the other. By contrast, vocals are often recorded *mono* and played equally in both channels.)

## *Thinking*

1. Lab0 作为第一个lab首先介绍了一些基础内容，如命令行的使用，程序设计，编码风格。
   1. 命令行作为计算机最初的操作方式，现在依然是计算机科学家日常使用的工具。主要原因大概是它比图形化操作界面更接近底层，且省去了开发图形化操作界面的资源。
   2. 程序设计中最关键的是抑制住立即开始写代码的冲动，先作计划和设计。这在一切的劳作中都是提升效率和结果的关键。
   3. 设计风格使得程序易于阅读、维护和复用（同样是对于未来的自己）。

2. 这个lab的主题是对于声音的处理。现实世界的声音在计算机中被表现为码率和各声道的一连串数字，这些数字即为气压的表达。对于这些数字系统化的处理便可以创造特定的音效或希望的结果。













