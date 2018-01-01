The shortest yet efficient implementation of [PrefixSpan](http://www.cs.sfu.ca/~jpei/publications/span.pdf) in Python 3, in less than 15 lines in core part. You can find the Scala version [here](https://github.com/chuanconggao/PrefixSpan-scala).

# Usage
```
prefixspan.py (frequent | top-k) <threshold> [--minlen=1] [--maxlen=maxint] [<file>]
```

  * Sequences are read from standard input. Each sequence is integers separated by space, like this example:
```
0 1 2 3 4
1 1 1 3 4
2 1 2 2 0
1 1 1 2 2
```

  * The patterns and their respective frequencies are printed to standard output.

# Features
Outputs traditional single-item sequential patterns, where gaps are allowed between items.

  * Mining top-k patterns is also supported, with respective optimizations.
  * You can also limit the length of mined patterns. Note that setting maximum pattern length properly can significantly speedup the algorithm.

# Tip
I strongly encourage using PyPy instead of CPython to run the script for best performance. In my own experience, it is nearly 10 times faster in average.
