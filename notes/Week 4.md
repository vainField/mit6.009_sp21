# <u>L4. Recursive Patterns</u>

In a general sense, recursion occurs when a thing is defined in terms of itself.

To solve a problem recursively, we typically identify:

- One or more base cases (a terminating scenario that does not use recursion to produce an answer), and
- One or more recursive cases (a set of rules that reduce all other cases toward the base case).

## Recursion vs Iteration?

```python
def factorial(n):
	if n == 0:
		return 1
	return n * factorial(n - 1)

def factorial(n):
	out = 1
	for i in range(1, n+1):
		out *= i
	return out
```

Do we even need recursion?

```python
def can_log(x):
    """
    Checks whether a given value can be a log entry.
    Valid log entries are strings/bytestrings, ints, floats, complex numbers,
    None, or Booleans; _or_ lists, tuples, sets, frozensets, dicts, or
    OrderedDicts containing only valid log entries.
    """
    if isinstance(x, (str, bytes, int, float, complex, NoneType, bool)):
        return True
    elif isinstance(x, (list, tuple, set, frozenset)):
        return all(can_log(i) for i in x)
    elif isinstance(x, (dict, OrderedDict)):
        return all((can_log(k) and can_log(v)) for k,v in x.items())
    return False
```

## Generator (生成器)

constant memory usage instead of linear memory usage of list

```python
# list
def list_range(start, end):
    out = []
    while start < end:
        out.append(start)
        start += 1
    return out

# generator
def gen_range(start, end):
    while start < end:
        yield start
        start += 1
        
print([i for i in gen_range(1, 10)])
```

## Doctest (测试模块)

```python
def average(values):
    """
    Computes the arithmetic mean of a list of numbers.

    >>> print(average([20, 30, 70]))
    40.0
    """
    return sum(values) / len(values)

import doctest
doctest.testmod()   # 自动验证嵌入测试
```





## *Thinking*

1. Lecture4 开始介绍递归，递归即自己调用自己，镜子中的镜子。和循环相比有什么不同的地方吗？可以这么看，循环是从底层开始建构，递归是从顶层开始寻找，因此循环更适合已知的结构，递归比较容易应对未知结构的问题。

   1. 例如：

      ```
      @instrument
      def depth_tree(tree):
          """ Walk a tree, returning the depth of the tree
          >>> depth_tree([13, [7], [8, [99], [16, [77]], [42]]])
          4
          """
          children = tree[1:]
          if children == []: return 1
          return 1 + max(depth_tree(child) for child in children)
      ```
      
   2. while循环或许可以处理未知结构的问题，但是逻辑上不如递归优雅

2. 还介绍了Doctest和Generator

# <u>R4. Recursion and Recursive Patterns</u>

## Decorator

“Decorators dynamically alter the functionality of a function, method, or class without having to directly use subclasses or change the source code of the function being decorated.”

### Instrument Decorator

Function entry and exit (our @instrument decorator): A printed version of call entries and exits, with recursion depth shown by indentation.

## *Thinking*

Recitation4 介绍了递归Recursion的一些实例，有两个要点：

1. 递归由两部分组成：base case 和 recursive case，base case要囊括所有recursive case无法处理的尽端情况。
2. 递归适用于层层相似的结构，例如除去第一个元素的list还是一个list，除去root node的tree是若干个tree，算法的设计也基于此。



# <u>Lab4. Frugal Maps</u>

## Data

[OpenStreetMap](https://en.wikipedia.org/wiki/OpenStreetMap): [OSM XML Format](https://wiki.openstreetmap.org/wiki/OSM_XML)

Nodes:

- `'id'` maps to an integer ID number for the node.
- `'lat'` maps to the node's latitude (in degrees).
- `'lon'` maps to the node's longitude (in degrees).
- `'tags'` maps to a dictionary containing additional information about the node, including information about the type of object represented by the node (traffic lights, speed limit signs, etc.).

Ways:

- `'id'` maps to an integer ID number for the way.
- `'nodes'` maps to a list of integers representing the nodes that comprise the way (in order).
- `'tags'` maps to a dictionary containing additional information about the way (e.g., is this a one-way street? is it a highway or a pedestrian path? etc.).

## Shortest Path

### Graph Search (BFS/DFS)

- Initialize an "agenda" (containing paths to consider)

- Initialize "visited" set (set of vertices we've ever added to the agenda) to contain only the starting vertex

- Repeat the following:

  - Remove one path from the agenda
  - If this path's terminal vertex satisfies the goal condition, return that path (hooray!)
  - For each of the children of that path's terminal vertex:
    - If it is in the visited set, skip it
    - Otherwise, add the associated path to agenda and add its vertex to visited set

  until agenda is empty (search failed)

#### A Weighty Problem

*uniform-cost search* (UC search)

- Initialize an "agenda" (containing paths to consider, as well as their costs).

- Intialize **empty** "expanded" set (set of vertices we've ever **removed from the agenda**)

- Repeat the following:

  - Remove **the path with the lowest cost** from the agenda.
  - **If this path's terminal vertex is in the expanded set**, ignore it completely and move on to the next path.
  - If this path's terminal vertex satisfies the goal condition, return that path (hooray!). Otherwise, **add its terminal vertex to the expanded set.**
  - For each of the children of that path's terminal vertex:
    - **If it is in the expanded set**, skip it
    - Otherwise, add the associated path (and cost) to the agenda

  until the agenda is empty (search failed)

## Heuristic

### Heuristics and Optimality

- a heuristic is admissible if it never overestimates the cost of the optimal path from any node to the goal, i.e., for all nodes $n$ :
  $h(n) \leq c^{*}(n)$
  where $c^{*}(n)$ represents the actual cost of the least-cost path to the goal.
- a heuristic is consistent if the value of the heuristic never increases as we get closer to the goal. More precisely, a heuristic is consistent if, for each node $n$ and each successor $n^{\prime}$ of that node, the heuristic evaluated at $n$ is no more than the heuristic evaluated at $n^{\prime}$ plus the cost of traveling directly from $n$ to $n^{\prime}$ :
  $h(n) \leq c\left(n, n^{\prime}\right)+h\left(n^{\prime}\right)$

### Test

- 76,773 steps with heuristic
- 386,255 steps without heuristic



## *Thinking*

1. 一个重要的debug情况，小数据集上的测试没有出现问题，但是在大数据集上出现问题，但大数据集难以测试。方法为将所有function的small test打印出来，找出问题：
   1. 在数据处理中将latitude和longitude输入为相同的 `'lat'`，导致位置错误，但没有影响到小数据集上的测试
   2. 在UC search中没有将端节点出现过的路径排除，在小数据集上的测试时间尚可，数据集稍大即无法在有限时间内输出结果
2. 抽象、模块化：将功能尽可能的抽象，得到更为泛用的功能。（黑箱化）
   1. 设置heuristic_ucs函数，将此搜索算法抽象
      1. 设置min_val函数，将priority queue功能抽象
3. 回顾一下这个lab
   1. 首先是数据结构的预处理，这个问题在lab3中已经显示出其重要性，lab4相对而言数据更为复杂，因此有更多的嵌套
      1. 需要做笔记把数据结构记录下来
   2. 然后开始处理搜索算法，本质上是有启发函数的uniform-cost search，如果对这个算法比较熟悉的话应该可以快速完成。
      1. 是否应该先了解算法再编写代码，这样应该会有更高的效率













