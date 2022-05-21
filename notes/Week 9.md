# <u>Lab9. snek 🐍</u>

## LISP (LISt Processor)

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

```lisp
(:= (fib n)
    (if (<= n 1)
      n
      (+ (fib (- n 1)) (fib (- n 2)))
    )
  )
```

- LISP consists only of expressions, with no statements. Every expression evaluates to a value.
- LISP uses prefix notation, e.g., `(+ 3 2)` instead of `3 + 2`.
- LISP's syntax is simpler but consists of a lot more parentheses.

## Interpreter Design

- A *tokenizer*, which takes a string as input and produces a list of *tokens*, which represent meaningful units in the syntax of the programming language.
- A *parser*, which takes the output of the tokenizer as input and produces a structured representation of the program as its output.
- An *evaluator*, which takes the output of the parser as input and actually handles running the program.

## *Thinking*

Lab9 尝试编写一个LISP语言的解释器，取名为snek。主要的目的是理解语言的设计，scoping的概念，对function的更为深入的理解，等等。

在编写的过程中有大量的设计决定要做：从大了说，哪些def，哪些class；往细了说，class里哪些attribute，哪些method，funciton里的条件语句的分类方式，哪些写成helper function等等。

这些大概需要大量的经验和总结。















