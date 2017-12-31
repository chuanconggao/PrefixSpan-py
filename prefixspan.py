#! /usr/bin/env python3

"""
Usage:
    prefixspan.py (frequent | top-k) <threshold> [<file>] [--minlen=1] [--maxlen=maxint]
"""

# Uncomment for static type checking
# from typing import *
# Matches = List[Tuple[int, int]]
# Pattern = List[int]
# Results = List[Tuple[int, Pattern]]

import sys
from collections import defaultdict
from heapq import heappop, heappush

from docopt import docopt

__minlen, __maxlen = 1, sys.maxsize

results = [] # type: Results

def __scan(matches):
    # type: (Matches) -> DefaultDict[int, Matches]
    alloccurs = defaultdict(list) # type: DefaultDict[int, Matches]

    for (i, pos) in matches:
        seq = db[i]

        occurs = {} # type: Dict[int, int]
        for j in range(pos, len(seq)): # Use xrange in Python 2
            occurs.setdefault(seq[j], j + 1)

        for k, newpos in occurs.items(): # Use .iteritems() in Python 2
            alloccurs[k].append((i, newpos))

    return alloccurs


def frequent_rec(patt, matches):
    # type: (Pattern, Matches) -> None
    if len(patt) >= __minlen:
        results.append((len(matches), patt))

        if len(patt) == __maxlen:
            return

    for (c, newmatches) in __scan(matches).items(): # Use .iteritems() in Python 2
        if len(newmatches) >= minsup:
            frequent_rec(patt + [c], newmatches)


def topk_rec(patt, matches):
    # type: (Pattern, Matches) -> None
    if len(patt) >= __minlen:
        heappush(results, (len(matches), patt))
        if len(results) > k:
            heappop(results)

        if len(patt) == __maxlen:
            return

    for (c, newmatches) in sorted(
            __scan(matches).items(), # Use .iteritems() in Python 2
            key=(lambda x: len(x[1])),
            reverse=True
        ):
        newpatt = patt + [c]
        if len(results) == k and (len(newmatches), newpatt) <= results[0]:
            break

        topk_rec(newpatt, newmatches)


if __name__ == "__main__":
    def checkArg(arg, cond):
        # type: (str, Callable[[int], bool]) -> int
        threshold = int(argv[arg])
        if cond(threshold):
            return threshold

        print("ERROR: {} is not in correct range.".format(arg), file=sys.stderr)
        sys.exit(1)


    argv = docopt(__doc__)

    db = [
        [int(v) for v in line.rstrip().split(' ')]
        for line in (open(argv["<file>"]) if argv["<file>"] else sys.stdin)
    ]

    if argv["frequent"]:
        minsup = checkArg("<threshold>", lambda v: 0 < v <= len(db))
        func = frequent_rec
    elif argv["top-k"]:
        k = checkArg("<threshold>", lambda v: v > 0)
        func = topk_rec

    if argv["--minlen"]:
        __minlen = checkArg("--minlen", lambda v: v > 0)
    if argv["--maxlen"]:
        __maxlen = checkArg("--maxlen", lambda v: v >= __minlen)

    func([], [(i, 0) for i in range(len(db))]) # Use xrange in Python 2

    if argv["top-k"]:
        results.sort(key=(lambda x: -x[0]))
    for (freq, patt) in results:
        print("{} : {}".format(' '.join(str(v) for v in patt), freq))
