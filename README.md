[![PyPI version](https://img.shields.io/pypi/v/prefixspan.svg)](https://pypi.python.org/pypi/prefixspan/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/prefixspan.svg)](https://pypi.python.org/pypi/prefixspan/)
[![PyPI license](https://img.shields.io/pypi/l/prefixspan.svg)](https://pypi.python.org/pypi/prefixspan/)

The shortest yet efficient implementation of the famous frequent sequential pattern mining algorithm [PrefixSpan](https://ieeexplore.ieee.org/abstract/document/914830/), the famous frequent **closed** sequential pattern mining algorithm [BIDE](https://ieeexplore.ieee.org/abstract/document/1319986) (in `closed.py`), and the frequent **generator** sequential pattern mining algorithm [FEAT](https://dl.acm.org/citation.cfm?doid=1367497.1367651) (in `generator.py`), as a unified and holistic algorithm framework.

- BIDE is usually much faster than PrefixSpan on large datasets, as only a small subset of closed patterns sharing the equivalent information of all the patterns are returned.

- FEAT is usually faster than PrefixSpan but slower than BIDE on large datasets.

For simpler code, some general purpose functions have been moved to be part of a new library [extratools](https://github.com/chuanconggao/extratools).

## Reference

### Research Papers

``` text
PrefixSpan: Mining Sequential Patterns by Prefix-Projected Growth.
Jian Pei, Jiawei Han, Behzad Mortazavi-Asl, Helen Pinto, Qiming Chen, Umeshwar Dayal, Meichun Hsu.
Proceedings of the 17th International Conference on Data Engineering, 2001.
```

``` text
BIDE: Efficient Mining of Frequent Closed Sequences.
Jianyong Wang, Jiawei Han.
Proceedings of the 20th International Conference on Data Engineering, 2004.
```

``` text
Efficient mining of frequent sequence generators.
Chuancong Gao, Jianyong Wang, Yukai He, Lizhu Zhou.
Proceedings of the 17th International Conference on World Wide Web, 2008.
```

### Alternative Implementations

I created this project with the [original](https://github.com/chuanconggao/PrefixSpan-py/commit/441b04eca2174b3c92f6b6b2f50a30f1ffe4968c) minimal 15 lines implementation of PrefixSpan for educational purpose. However, as this project grows into a full feature library, its code size also inevitably grows. I have revised and reuploaded the original implementation as a GitHub Gist [here](https://gist.github.com/chuanconggao/4df9c1b06fa7f3ed854d5d96e2ae499f) for reference.

You can also try my Scala [version](https://github.com/chuanconggao/PrefixSpan-scala) of PrefixSpan.

## Features

Outputs traditional single-item sequential patterns, where gaps are allowed between items.

- Mining top-k patterns is supported, with respective optimizations on efficiency.

- You can limit the length of mined patterns. Note that setting maximum pattern length properly can significantly speedup the algorithm.

- Custom key function, custom filter function, and custom callback function can be applied.

## Installation

This package is available on PyPI. Just use `pip3 install -U prefixspan` to install it.

## CLI Usage

You can simply use the algorithms on terminal.

``` text
Usage:
    prefixspan-cli (frequent | top-k) <threshold> [options] [<file>]

    prefixspan-cli --help


Options:
    --text             Treat each item as text instead of integer.

    --closed           Return only closed patterns.
    --generator        Return only generator patterns.

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

- When dealing with text data, please use the `--text` option. Each sequence is words separated by space, assuming stop words have been removed, like this example:

``` text
cat test.txt

a b c d e
b b b d e
c b c c a
b b b c c
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

``` text
prefixspan-cli frequent 2 --text test.txt

a : 2
b : 4
b c : 3
b c c : 2
b d : 2
b d e : 2
b e : 2
b b : 2
b b b : 2
c : 3
c c : 2
d : 2
d e : 2
e : 2
```

## API Usage

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

print(ps.topk(5, closed=True))


print(ps.frequent(2, generator=True))

print(ps.topk(5, generator=True))
```

## Closed Patterns and Generator Patterns

The closed patterns are much more compact due to the smaller number.

- A pattern is closed if there is no super-pattern with the same frequency.

``` text
prefixspan-cli frequent 2 --closed test.dat

0 : 2
1 : 4
1 2 : 3
1 2 2 : 2
1 3 4 : 2
1 1 1 : 2
```

The generator patterns are even more compact due to both the smaller number and the shorter lengths.

- A pattern is generator if there is no sub-pattern with the same frequency.

- Due to the high compactness, generator patterns are useful as features for classification, etc.

``` text
prefixspan-cli frequent 2 --generator test.dat

0 : 2
1 1 : 2
2 : 3
2 2 : 2
3 : 2
4 : 2
```

There are patterns that are both closed and generator.

``` text
prefixspan-cli frequent 2 --closed --generator test.dat

0 : 2
```

## Custom Key Function

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

## Custom Filter Function

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

## Custom Callback Function

For both the frequent and the top-k algorithm, you can use a custom callback function `callback=lambda patt, matches: ...` instead of returning the normal results of patterns and their respective frequencies.

- When callback function is specified, `None` is returned.

- For large datasets, when mining frequent patterns, you can use callback function to process each pattern immediately, and avoid having a huge list of patterns consuming huge amount of memory.

- The following example finds the longest frequent pattern covering each sequence.

``` python
coverage = [[] for i in range(len(db))]

def cover(patt, matches):
    for i, _ in matches:
        coverage[i] = max(coverage[i], patt, key=len)


ps.frequent(2, callback=cover)

print(coverage)
# [[1, 3, 4],
#  [1, 3, 4],
#  [1, 2, 2],
#  [1, 2, 2]]
```

## Tip

I strongly encourage using [PyPy](http://pypy.org/) instead of CPython to run the script for best performance. In my own experience, it is nearly 10 times faster in average. To start, you can install this package in a [virtual environment](https://virtualenv.pypa.io/en/stable/) created for PyPy.
