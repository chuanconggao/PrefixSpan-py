[![PyPI version](https://badge.fury.io/py/prefixspan.svg)](https://badge.fury.io/py/prefixspan)

The shortest yet efficient implementation of [PrefixSpan](http://www.cs.sfu.ca/~jpei/publications/span.pdf) in Python 3, with less than 20 lines in core part (scan and extend). You can also try the Scala [version](https://github.com/chuanconggao/PrefixSpan-scala).

It is very simple to use this package under Python 2. You only need to tweak 2-3 lines.

# Installation

This package is available on PyPi. Just use `pip3 install -U prefixspan` to install it.

# CLI Usage

You can simply use the algorithm on terminal.

```
Usage:
    prefixspan-cli (frequent | top-k) <threshold> [options] [<file>]

    prefixspan-cli --help


Options:
    --minlen=<minlen>  Minimum length of patterns. [default: 1]
    --maxlen=<maxlen>  Maximum length of patterns. [default: 1000]

    --key=<key>        Custom key function for top-k algorithm. [default: ]
                       Must be a Python lambda function in form of "lambda patt, matches: ...".
```

* Sequences are read from standard input. Each sequence is integers separated by space, like this example:

```
0 1 2 3 4
1 1 1 3 4
2 1 2 2 0
1 1 1 2 2
```

* The patterns and their respective frequencies are printed to standard output.

```
0 : 2
1 : 4
1 2 : 3
1 2 2 : 2
1 3 : 2
1 3 4 : 2
1 4 : 2
1 1 : 2
1 1 1 : 2
2 : 3
2 2 : 2
3 : 2
3 4 : 2
4 : 2
```

# API Usage

Alternatively, you can use the algorithm via API.

- For top-k algorithm, a custom key function `key=lambda patt, matches: ...` can be applied, where `patt` is the current pattern and `matches` is the current list of matching sequence IDs.
    
    - In default, `len(matches)` is used denoting the support of current pattern.

    - Alternatively, as an example, `len(patt) if len(matches) >= threshold else 0` can be used to find the k longest frequent patterns.

``` python
from prefixspan import PrefixSpan

db = [
    [0, 1, 2, 3, 4],
    [1, 1, 1, 3, 4],
    [2, 1, 2, 2, 0],
    [1, 1, 1, 2, 2],
]

ps = PrefixSpan(db)

print(ps.frequent(2))
# [(2, [0]),
#  (4, [1]),
#  (3, [1, 2]),
#  (2, [1, 2, 2]),
#  (2, [1, 3]),
#  (2, [1, 3, 4]),
#  (2, [1, 4]),
#  (2, [1, 1]),
#  (2, [1, 1, 1]),
#  (3, [2]),
#  (2, [2, 2]),
#  (2, [3]),
#  (2, [3, 4]),
#  (2, [4])]

print(ps.topk(5))
# [(4, [1]),
#  (3, [2]),
#  (3, [1, 2]),
#  (2, [1, 3]),
#  (2, [1, 3, 4])]

ps.topk(5, key=lambda patt, matches: len(patt) if len(matches) >= 2 else 0)
# [(3, [1, 2, 2]),
#  (3, [1, 3, 4]),
#  (2, [1, 2]),
#  (2, [1, 3]),
#  (2, [1, 4])]
```

# Features

Outputs traditional single-item sequential patterns, where gaps are allowed between items.

    * Mining top-k patterns is also supported, with respective optimizations on efficiency.
  
    * You can also limit the length of mined patterns. Note that setting maximum pattern length properly can significantly speedup the algorithm.

# Tip

I strongly encourage using [PyPy](http://pypy.org/) instead of CPython to run the script for best performance. In my own experience, it is nearly 10 times faster in average. To start, you can install this package in a [virtual environment](https://virtualenv.pypa.io/en/stable/) created for PyPy.
