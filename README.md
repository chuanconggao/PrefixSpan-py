[![PyPi version](https://img.shields.io/pypi/v/prefixspan.svg)](https://pypi.python.org/pypi/prefixspan/)
[![PyPi pyversions](https://img.shields.io/pypi/pyversions/prefixspan.svg)](https://pypi.python.org/pypi/prefixspan/)
[![PyPi license](https://img.shields.io/pypi/l/prefixspan.svg)](https://pypi.python.org/pypi/prefixspan/)

The shortest yet efficient implementation of famous frequent sequential pattern mining algorithm [PrefixSpan](https://ieeexplore.ieee.org/abstract/document/914830/) in Python 3, with less than 20 lines in core part (scan and extend).

- You can also try the Scala [version](https://github.com/chuanconggao/PrefixSpan-scala).

Also includes the implementation of famous frequent **closed** sequential pattern mining algorithm [BIDE](https://ieeexplore.ieee.org/abstract/document/1319986), which extends the framework of PrefixSpan algorithm.

- A pattern is closed if there is no super-pattern with the same frequency.

- BIDE is usually much faster than PrefixSpan on large datasets, as only a small subset of closed patterns sharing the equivalent information of all the patterns are returned.

# Features

Outputs traditional single-item sequential patterns, where gaps are allowed between items.

- Mining top-k patterns is supported, with respective optimizations on efficiency.

- You can limit the length of mined patterns. Note that setting maximum pattern length properly can significantly speedup the algorithm.

- Custom key function and custom filter function can be applied.

# Installation

This package is available on PyPi. Just use `pip3 install -U prefixspan` to install it.

# CLI Usage

You can simply use the algorithms on terminal.

``` text
Usage:
    prefixspan-cli (frequent | top-k) <threshold> [options] [<file>]

    prefixspan-cli --help


Options:
    --closed           Return only closed patterns.

    --key=<key>        Custom key function. [default: ]
                       Must be a Python function in form of "lambda patt, matches: ...", returning an integer value.
    --bound=<bound>    The upper-bound function of the respective key function. When unspecified, the same key function is used. [default: ]
                       Must be no less than the key function, i.e. bound(patt, matches) ≥ key(patt, matches).
                       Must be anti-monotone, i.e. for patt1 ⊑ patt2, bound(patt1, matches1) ≥ bound(patt2, matches2).

    --filter=<filter>  Custom filter function. [default: ]
                       Must be a Python function in form of "lambda patt, matches: ...", returning a boolean value.

    --minlen=<minlen>  Minimum length of patterns. [default: 1]
    --maxlen=<maxlen>  Maximum length of patterns. [default: 1000]
```

* Sequences are read from standard input. Each sequence is integers separated by space, like this example:

``` text
cat test.dat

0 1 2 3 4
1 1 1 3 4
2 1 2 2 0
1 1 1 2 2
```

* The patterns and their respective frequencies are printed to standard output.

``` text
prefixspan-cli frequent 2 test.dat

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

* As you can see, the closed patterns are much more compact.

``` text
prefixspan-cli frequent 2 --closed test.dat

0 : 2
1 : 4
1 2 : 3
1 2 2 : 2
1 3 4 : 2
1 1 1 : 2
```

# API Usage

Alternatively, you can use the algorithms via API.

``` python
from prefixspan import PrefixSpan

db = [
    [0, 1, 2, 3, 4],
    [1, 1, 1, 3, 4],
    [2, 1, 2, 2, 0],
    [1, 1, 1, 2, 2],
]

ps = PrefixSpan(db)
```

For details of each parameter, please refer to the `PrefixSpan` class in `prefixspan/api.py`.

``` python
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


print(ps.frequent(2, closed=True))
# [(2, [0]),
#  (4, [1]),
#  (3, [1, 2]),
#  (2, [1, 2, 2]),
#  (2, [1, 3, 4]),
#  (2, [1, 1, 1])]

print(ps.topk(5, closed=True))
# [(4, [1]),
#  (3, [1, 2]),
#  (2, [1, 1, 1]),
#  (2, [1, 2, 2]),
#  (2, [1, 3, 4])]
```

# Custom Key Function

For both frequent and top-k algorithms, a custom key function `key=lambda patt, matches: ...` can be applied, where `patt` is the current pattern and `matches` is the current list of matching sequence `(id, position)` tuples.
    
- In default, `len(matches)` is used denoting the frequency of current pattern.

- Alternatively, any key function can be used. As an example, `sum(len(db[i]) for i in matches)` can be used to find the satisfying patterns according to the number of matched items.

- For efficiency, an anti-monotone upper-bound function should also be specified for pruning.

    - If unspecified, the key function is also the upper-bound function, and must be anti-monotone.

``` python
print(ps.topk(5, key=lambda patt, matches: sum(len(db[i]) for i, _ in matches)))
# [(20, [1]),
#  (15, [2]),
#  (15, [1, 2]),
#  (10, [1, 3]),
#  (10, [1, 3, 4])]
```

# Custom Filter Function

For both frequent and top-k algorithms, a custom filter function `filter=lambda patt, matches: ...` can be applied, where `patt` is the current pattern and `matches` is the current list of matching sequence `(id, position)` tuples.

- In default, `filter` is not applied and all the patterns are returned.

- Alternatively, any function can be used. As an example, `matches[0][0] > 0` can be used to exclude the patterns covering the first sequence.

``` python
print(ps.topk(5, filter=lambda patt, matches: matches[0][0] > 0))
# [(2, [1, 1]),
#  (2, [1, 1, 1]),
#  (2, [1, 2, 2]),
#  (2, [2, 2]),
#  (1, [1, 2, 2, 0])]
```

# Tip

I strongly encourage using [PyPy](http://pypy.org/) instead of CPython to run the script for best performance. In my own experience, it is nearly 10 times faster in average. To start, you can install this package in a [virtual environment](https://virtualenv.pypa.io/en/stable/) created for PyPy.
