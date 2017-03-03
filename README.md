The shortest yet efficient PrefixSpan implementation in Python, in only 20 lines in core part.

# Usage
Just replace the variable `db` with your own sequences, and variable `minsup` with your own minimum support threshold.

# Features
Based on state-of-the-art [PrefixSpan](http://www.cs.sfu.ca/~jpei/publications/span.pdf) algorithm.
Mining top-k patterns is also supported.

# Tip
I strongly encourage using PyPy instead of CPython to run the script for best performance. In my own experience, it is 9x times faster in average.
