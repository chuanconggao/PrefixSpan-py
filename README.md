The shortest yet efficient PrefixSpan implementation in Python, in only 12 lines in core part.

# Usage
```
prefixspan.py (frequent | top-k) <threshold>
```

In default, sequences are read from standard input and stored in the `db` variable. You can easily change the `db` variable for your own case.

# Features
Based on state-of-the-art [PrefixSpan](http://www.cs.sfu.ca/~jpei/publications/span.pdf) algorithm.
Mining top-k patterns is also supported.

# Tip
I strongly encourage using PyPy instead of CPython to run the script for best performance. In my own experience, it is 9x times faster in average.
