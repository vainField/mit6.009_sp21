# <u>L3. Graphs and Graph Search</u>

see 6.042

# <u>R3. Search Solutions</u>

## algorithm for bread-first or depth-first search

```python
from table import notebook_table #visualization

def search(start, is_goal, successors, dfs=False):
    """ Search for and return a node satisfying a goal
    
    start: the starting node
    is_goal(node): returns True if node satisfies the goal
    successors(node): a sequence of successor nodes to node
    
    Uses a list to keep track of an agenda of nodes to try
    
    Uses bfs by default, or dfs if specified
    """
    agenda = [start]   ## agenda[] includes all options to consider
    ## use list so that there is a sequence
    seen = {start}   ## implement seen{} to exclude redundant paths to node
    ## use set for seen{} so that there is no duplication and search is more efficient
    print_in_table = notebook_table('seen', 'agenda', 'node =')
    while agenda:
        print_in_table(seen)
        print_in_table(agenda)
        node = agenda.pop(-1 if dfs else 0)   ## next agenda item
        ## dfs: last in first out; bfs: last in last out
        print_in_table(node)
        if is_goal(node):   ## define is_goal() function in examples to define the goal
            return node
        for s in successors(node):   ## define successors() function in examples to define possible adjoining nodes
            if s not in seen:
                agenda.append(s)   ## list uses append() since there is a sequence
                seen.add(s)   ## set uses add() since there is no sequence
```

```python
graph1 = {'root': [13, ['A', 'B', 'C']],
          'A': [77, ['D', 'E']],
          'B': [42, []],      ## a node contains a value and a list of adjoining nodes
          'C': [0, ['G']],
          'D': [-32, ['F']],
          'E': [42, ['F']],
          'F': [215, []],
          'G': [8, []],
}
```

```python
def example_3(dfs):
    start = 'root'
    goal_value = 42
    
    def is_goal(node):   ## definition of is_goal()
        return graph1[node][0] == goal_value

    def successors(node):   ## definition of successors()
        return graph1[node][1]

    result = search(start, is_goal, successors, dfs=dfs)
    notebook_table.display()
```

## a `search_path` capability to find a path

simply put all possible paths as tuples in `agenda[]`

```python
agenda = [(start,)]
# codes
while ...
    for s in successors(node):
        if s not in seen:
            agenda.append(path + (s,))
```

tuple is like int, use `+` instead of `append()` or `add()`

initiate a tuple by `(0,)`, where `,` is obligatory for single element tuple

## Word Ladder

search in list and tuple: linear time vs. constant time

```python
def successors(word): # time: 19.1268253326416 sec
    succ_words = []
    for succ_word in allwords: # linear time of len(all_words): 558903
        if len(succ_word) == len(word) and len([i for i, j in zip(succ_word, word) if i!= j]) == 1:
            succ_words.append(succ_word)
    return succ_words

def successors(word): # time: 1.132817029953003  
    new_words = set()
    for i in range(len(word)): # linear time of len(ALL_Letters): 26
        for letter in ALL_LETTERS:
            maybe = word[:i] + letter + word[i+1:]
            if maybe in allwords: # constant time
                new_words.add(maybe)
    return new_words
```

## *Thinking*

Recitation3 将讲座中讨论的搜索算法通过python编程出来。有两个有趣的地方，一个是数据类型，一个是抽象和继承。

1. 对于数据类型的使用是重要的，不同的数据类型有不同的用法，只是简单的数据集也有很重要的差别：是否有序，是否可以有重复元素，搜索的复杂度等等，都影响着算法的有效性和效率。
2. 抽象和继承使得程序更为范用，例如这里的搜索函数，可以被应用到各种实例。

# <u>Lab3. Bacon Number</u>

## 1. Framework

### 1.1. Transforming the Data +_+

in order to accelerate  manipulations

<u>***we only call `transform_data` once per movie database, so the work you do transforming can pay off to support multiple fast operations thereafter!***</u>

### 1.2. Acting Together

#### a small excercise to get familiar with the database

if two actors have acted together

**a small test**

### 1.3. Bacon Number

to find all of the actors who have a given Bacon number

to generalize to getting the *Bacon number* `i+1` actors from the *Bacon number* `i` actors.

**small tests**

### 1.4. Paths

#### 1.4.1. Bacon Path

**a small test**

##### 1.4.1.1. Speed

1. a single dictionary lookup or set-containment check instead of `for`
2. `in` for sets and dictionaries instead of for lists
3. use an index to keep track of which list element you’re working on instead of use `L.pop(0)` on a long list

***avoid repeatedly iterating through all of `data` !!!***

#### 1.4.2. Arbitray Paths

 `actor_to_actor_path` 

**a test case**

##### make helper functions

### 1.5. Movie Paths

### 1.6. Generalizing the Path Finder

the shortest path from some actor to *any actor from a set of other actors*, or from some actor to *any actor in a particular movie*, or something like that.

### 1.7. Movie-to-Movie Paths

chains of actors that connect one given *movie* to another

## 2. Test Design

Tiny test database

Compute test responces manually

## *Thinking*

1. 每一个lab都在逐渐复杂，但是抽象（Abstraction）确实是简化的非常有效的方法。一定的抽象可以使得特定算法有能力应对更多的问题。
   1. 例如breadth fisrst search，将目标和继承作为搜索函数的变量，它们本身在实例化时又可以被定义为函数。
   2. Lab3 即是一个逐步抽象化的练习，后一个练习往往可以被前一个练习调用从而简化前一个练习。在这个过程中便可以感受到抽象的力量。
2. Lab3 加上Recitation3 第一次详细讨论了程序的效率
   1. 不同的算法由不同的数据类型进行优化
   2. 对于原始数据集进行处理将会使得之后所有在此数据集上的操作变得更快，因此非常有价值。我这次的做法是针对之后的不同类型的操作进行了不同的处理。
   3. 有些功能例如L.pop()虽然有用但在一些情况下（Lab3这里即长列表）速度很慢，需要尽可能避免使用，寻找其他替代的方法
   4. 一些小的优化，例如Rec3中重复复制set/list从效率上低于先嵌套再在最后展开



