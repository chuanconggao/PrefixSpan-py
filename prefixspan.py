#! /usr/bin/env python3

"""
Usage:
    prefixspan.py (frequent | top-k) <threshold> [--minlen=1] [--maxlen=maxint] [<file>]
"""

# Uncomment for static type checking
# from typing import *
# Matches = List[Tuple[int, int]]
# Pattern = List[int]
# Results = List[Tuple[int, Pattern]]

import sys
from collections import defaultdict
from heapq import heappop, heappush


__minlen, __maxlen = 1, sys.maxsize

results = [] # type: Results
__db = []
__k = 0
__minsup = 0

def __scan(matches):
    # type: (Matches) -> DefaultDict[int, Matches]
    alloccurs = defaultdict(list) # type: DefaultDict[int, Matches]

    for (i, pos) in matches:
        seq = __db[i]

        occurs = set() # type: Set[int]
        for j in range(pos, len(seq)):
            k = seq[j]
            if k not in occurs:
                occurs.add(k)
                alloccurs[k].append((i, j + 1))

    return alloccurs


def frequent_rec(patt, matches):
    # type: (Pattern, Matches) -> None
    if len(patt) >= __minlen:
        results.append((len(matches), patt))

        if len(patt) == __maxlen:
            return

    for (c, newmatches) in __scan(matches).items():
        if len(newmatches) >= __minsup:
            frequent_rec(patt + [c], newmatches)


def topk_rec(patt, matches):
    # type: (Pattern, Matches) -> None
    if len(patt) >= __minlen:
        heappush(results, (len(matches), patt))
        if len(results) > __k:
            heappop(results)

        if len(patt) == __maxlen:
            return

    for (c, newmatches) in sorted(
            __scan(matches).items(),
            key=(lambda x: len(x[1])),
            reverse=True
        ):
        if len(results) == __k and len(newmatches) <= results[0][0]:
            break

        topk_rec(patt + [c], newmatches)


def find_pattern(db, funcname="top-k", k=3, minsup=3, minlen=__minlen, maxlen=__maxlen):
    global __db, __k, __minsup, results, __minlen, __maxlen
    
    __db=db
    __k = k
    __minsup = minsup
    results = []
    if funcname == "frequent":
        func = frequent_rec
    elif funcname == "top-k":
        func = topk_rec

    __minlen = minlen
    __maxlen = maxlen

    func([], [(i, 0) for i in range(len(db))])
    if funcname == "top-k":
        results.sort(key=(lambda x: -x[0]))
    for (freq, patt) in results:
        print("{} : {}".format(' '.join(str(v) for v in patt), freq))

