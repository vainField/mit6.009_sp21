# <u>L7. Custom Types and Environment Model</u>

## class

```python
class Vec2D:
	ndims = 2
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def mag(self):
		return (self.x**2 + self.y**2) ** 0.5
v = Vec2D(3, 4)
print(v.mag())
```

## Variable and Attribute Lookup

### Looking up a variable: 

1. look in the current frame first 
2. if not found, look in the parent frame 
3. if not found, look in that frame’s parent frame 
4. . . . 
5. if not found, look in the global frame 
6. if not found, look in the builtins 
7. if not found, raise a `NameError`

### Looking up an attribute (in an object, using ”dot” notation): 

1. look in the object itself 
2. if not found, look in that object’s class 
3. if not found, look in that class’s superclass 
4. if not found, look in that class’s superclass 
5. . . . 
6. if not found and no more superclasses, raise an `AttributeError`

## Self

- Additional weirdness: when looking up a class method by way of an instance, that instance will automatically be passed in as the first argument.

- For example, the following two pieces of code will do the same thing, if `x` is an instance of class `Foo`:

  ```python
  Foo.bar(x, 1, 2, 3)
  x.bar(1, 2, 3)
  ```

- By convention, this first parameter is usually called `self`. Even though it’s not strictly necessary, it’s a good idea to follow that convention.

## "Magic" Methods

Python offers ways to integrate things more tightly into the language: “magic” methods or “dunder” methods. For example: 

- `print(x)` is translated implicitly to `print(x.__str__())` 
- `abs(x)` is translated implicitly to `x.__abs__()` 
- `x + y` is translated implicitly to `x.__add__(y)` 
- `x - y` is translated implicitly to `x.__sub__(y)` 
- `x[y]` is translated implicitly to `x.__getitem__(y)` 
- `x[y] = z` is translated implicitly to `x.__setitem__(y, z)`

## *Thinking*

Lecture7 开始介绍class，没有太多的理论知识，主要是一种模块化的思想。由于涉及到多层的继承，需要关注变量和属性的查找顺序。

# <u>R7. Object-Oriented Design</u>

## *Thinking*

1. Recitation7 使用 War Card Game 这个例子延续 Lecture7 进行面对对象编程的复习。 

2. 不同类型的功能

   1. `__foo__`: system
   2. `__foo`: private (only used by the class)
   3. `_foo`: protected (only used by the class and its sub-classes)

3. 继承关系草图

   <img src="image.assets/Screen Shot 2021-05-15 at 15.20.58.png" alt="Screen Shot 2021-05-15 at 15.20.58" style="zoom: 33%;" />

# <u>Lab7. Autocomplete</u>

## Trie (prefix tree)

<img src="image.assets/Screen Shot 2021-05-20 at 11.03.03.png" alt="Screen Shot 2021-05-20 at 11.03.03" style="zoom:50%;" />



## *Thinking*



Lab7 利用数据结构 Trie (as in retrieval)来练习Class。Trie本身是较为抽象的数据结构，对于这类问题：

- 实际上如果可以先上网了解一下这种数据结构的情况应该可以节约大量时间和意志力。
- 可以先分析各元素的数据类型和互相之间的关系及操作的方式：node, edge, key, self.value, self.children, self.key_type...
  - 临时的想法：如果将这些元素/属性的关系和互相之间的操作画成diagram，对于下面的编码会有极大的帮助
- 看来Trie是逐元素搜索的典型结构，value保存在node之中，而edge/pointer及其指向的sub_nodes则保存为node.children字典。相比基础数据结构，应对特定问题在搜索过程中不需要遍历所有元素，更为高效
- Trie也是一种tree，因此也是典型的适用于递归的数据结构

这次Lab获得的经验：

- 对于递归函数，可以使用 `@instrument` 来进行test
- test（如doctest）中尽量包含所有可能，这样比较容易快速检查出错误，后期在大型实例上的调试只会更花时间
- 由于Trie中的edge为key中的单个元素，它们的数据类型的不同会很大程度上影响操作，过程中发现key的类型基本为`tuple`和`str`两种，只需对应edge的类型也为`tuple`和`str`，就可以使用`+`完成对于edge的合并，因此问题转换为一个helper function来处理从key中截取edge，如果`key_type`不在helper function中，则 `raise TypeError`
- 在递归和循环本身无法避免元素重复的情况下，可以先使用`set`找到所有不重复的元素，如有需要再转换为`list`

