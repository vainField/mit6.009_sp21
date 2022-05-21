# <u>L10. More Fun with Functions</u>

Lab 9: basics of evaluation (including function calls) 

Lab 10: conditionals, lists, and other nice things

### Why Bother Writing Interpreters? 

- It is just so cool!!! 
- It can help you understand the semantics of languages you already know (and contrast differing semantics). 
- There is something powerful about the idea that an interpreter (CPython, for example) is just another program

### Why LISP? 

- LISP is weird/cool :) 
  - ”A language that doesn’t affect the way you think about programming, is not worth knowing” -Alan Perlis 
- MIT and LISP have a long history 
  - invented here in 1958 (McCarthy) 
  - one widely-used dialect (Scheme) implemented here as well, used in 6.001 from ∼1980-2007 
- Generally has very minimal syntax, so we can spend less time thinking about tokenizing/parsing, and more time thinking about rules for evaluation.

# <u>R10. Python Variable Scoping and Closures</u>

## Scoping

#### ⇒ Idea 1: Python local variables shadow variables in surrounding scope

#### ⇒ Idea 2: How does python know a variable is local?

- If you **assign** a variable in a local scope, it is *local* and shadows the variable in the surrounding scope.
- If you **access** a local variable before it is assigned in the local scope, that causes an exception.

#### ⇒ Idea 3: How to assign a variable in the surrounding scope:

- Python **nonlocal** declaration tells python to use the variable in the *nearest* surrounding scope where that local variable exists, excluding global.
- Note that a **nonlocal** variable needs to exist in a surrounding scope, not including the global scope, else an exception is raised

#### ⇒ Idea 4: How to assign a variable in the global scope:

- Python **global** declaration tells python to use the variable in the global scope (skipping over any intervening nonlocal/surrounding scoped variables with that name whether they exist or not).
- In lab 10, snek does not have or ask you to implement a global declaration. Scheme and many versions of Lisp, however, do have this idea!

## Python Closure

The idea of a "closure" is that a function definition remembers the environment in which it was defined, so that later when the function is called, that function has access to the variables in the enclosing environment.

#### Closures enable object-oriented programming styles

In python, we have classes, methods, instances, etc., so those are very convenient for OOP. However, we could build something similar using the power of closures and local state. One such style is often referred to as **message passing**.

```python
def make_account(balance):
    def deposit(amount):
        nonlocal balance
        balance += amount
    def get_balance():
        return balance
    
    def methods(message):
        if message == 'deposit':
            return deposit
        elif message == 'balance':
            return get_balance
    return methods

jessie_acct = make_account(100)
jessie_acct('deposit')(10)
print(jessie_acct('balance')())
jessie_acct('deposit')(8000)
print(jessie_acct('balance')())
```



# <u>Lab10. Snek (Part II) 🐍🐍</u>

Lab10 继续进行snek的编写。有更多关于代码结构的练习和经验。有几个主要内容：

1. 基于cons cells的linked list
   - 由于对于linked list操作的函数不是直接由python语言调用，因此无法直接用Recursion的形式编写，经过一些尝试后采用了Iteration
2. built-in functions / custom functions / special forms
   - 对于expression的分类是一个较高层级的问题，在lab中某种程度上已经被教授决定
   - 解决问题的思路是一个非常重要的问题
3. 最后针对oop所写的`del`，`let`，`set!` 在Recitation中讲解了和scoping的关系，也是一个理解oop的角度
4. 清晰的代码结构对大型程序的影响极大，这个lab基本给出了一个可用的形式，可以作为以后的参考
   - `#`包围的文字作为大标题
   - `##`加上首字母大写文字作为第二层级的标题
   - `##`加上小写文字作为函数、类下的标题，配合indentation/序号使用
   - 问题较为复杂时将标题加上序号
   - 大量函数/类如何分组是一个悬置的问题，可能通过import解决
5. 整个问题的diagram也是十分必要的，有助于对整个问题的把握
   - 使用miro绘制草图

























