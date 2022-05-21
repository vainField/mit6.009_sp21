#  <u>L8. Custom Types and Linked Structures</u>



# <u>R8. OOP</u>

```python
x = "dog"

class A:
    x = "cat"

class B(A):
    x = "ferret" 
    def __init__(self):
        self.x = x 

b = B()   ## 在global environment中创建？
print('b.x:', b.x)

# b.x: dog
```



# <u>Lab8. Symbolic Algebra</u>

## Preparation

1. Try making a plan for your code, including the following:
   - Which classes are you going to implement? Which classes are subclasses of which classes?
   - What attributes are stored in each class?
   - What methods does each class have?
2. take advantage of inheritance to avoid repetitious code!
3. our goal is to use Python's own mechanism of method/attribute lookup to implement these different behaviors without the need to do any type checking of our own.

## *Thinking*

Lab8 使用符号代数训练了class的使用。有几点心得：

1. 关于class

   - 继承作为抽象的重要工具：例如对于符号代数，Num、Var、BinaryOperator都是Symbol，虽然Symbol本身并不需要 `__init__` ，但是很多函数都可以被子类共用，BinrayOperator又是Add、Sub等的超类，从而构建出多层级的继承关系

   - 需要了解更多的class中属性和函数的继承关系和调用顺序，看一下6.145中有没有相关内容，然后再复习Recitation中的内容
   - 可以使用Miro来进行class关联草图的绘制，一个mind map作为一个class，其他关联连线

2. 关于debug

   - 遇到困难时写下简单的例子是极好的方法
   - 自己做项目时尽量使用doctest穷尽简单参数的可能性









