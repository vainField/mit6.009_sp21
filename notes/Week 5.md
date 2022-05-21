# <u>Lab5. Mines</u>

## Refactoring

*"A designer knows he has achieved perfection not when there is nothing left to add, but when there is nothing left to take away."*
-Antoine de Saint-Exupéry

**DRY** principle (**D**on't **R**epeat **Y**ourself)

1. multiple fragments of code should not describe redundant logic. 
2. that logic can often be refactored to make use of a variable, a loop, or a function to avoid re-writing the same code multiple times.
3. if you find yourself re-writing the same short expression over and over, that might be a good sign that you can store that in a variable as an intermediate result. If you find yourself copy/pasting a block of code to compute a result, that might be an opportunity to define a function and/or to use a looping structure.

## Handling N-d Structures

- A function that, given an N-d array and a tuple/list of coordinates, returns the value at those coordinates in the array.
- A function that, given an N-d array, a tuple/list of coordinates, and a value, replaces the value at those coordinates in the array with the given value.
- A function that, given a list of dimensions and a value, creates a new N-d array with those dimensions, where each value in the array is the given value.
- A function that, given a game, returns the state of that game (`'ongoing'`, `'defeat'`, or `'victory'`).
- A function that returns (or a generator--introduced in week 5's lecture--that yields) all the neighbors of a given set of coordinates in a given game.
- A function that returns (or a generator that yields) all possible coordinates in a given board.

## *Thinking*

Lab5 没有太多的新内容，是在之前内容的整合上进一步进行训练。有几个要点和心得：

1. 比较全面地梳理问题的逻辑， 如扫雷：
   1. 棋局的状体可能有哪些：失败、成功、进行中
   2. 输入可能有哪些：已扫，未扫有雷，未扫无雷周围有雷，未扫无雷周围无雷
   3. 新的输入后棋局的状态是否有变化
   4. 新的输入后哪些区域会有改变
2. 校订：将重复的代码写为function、variable、loop等等
3. 抓住问题的难点并整理为helper functions（之后应为class）如多维问题：
   1. 得到坐标节点的值
   2. 修改坐标节点的值
   3. 初始化多维矩阵
   4. 得到坐标节点的相邻节点（生成器）
   5. 得到矩阵的所有坐标（生成器）



