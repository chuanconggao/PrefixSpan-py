#! /usr/bin/env python

"""
Usage:
    prefixspan.py (frequent | top-k) <threshold> [<file>] [--minlen=1] [--maxlen=maxint]
"""

from __future__ import print_function

import sys
from collections import defaultdict
from heapq import heappop, heappush

from docopt import docopt

__minlen, __maxlen = 1, sys.maxint

results = []

def __scan(patt, mdb):
    occurs = defaultdict(list)
    for (i, startpos) in mdb:
        seq = db[i]
        for j in xrange(startpos, len(seq)):
            l = occurs[seq[j]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, j + 1))

    return occurs


def frequent_rec(patt, mdb):
    if len(patt) >= __minlen:
        results.append((len(mdb), patt))

        if len(patt) == __maxlen:
            return

    for (c, newmdb) in __scan(patt, mdb).iteritems():
        if len(newmdb) >= minsup:
            frequent_rec(patt + [c], newmdb)


def topk_rec(patt, mdb):
    if len(patt) >= __minlen:
        heappush(results, (len(mdb), patt))
        if len(results) > k:
            heappop(results)

        if len(patt) == __maxlen:
            return

    for (c, newmdb) in sorted(
            __scan(patt, mdb).iteritems(),
            key=(lambda (c, newmdb): len(newmdb)),
            reverse=True
        ):
        newpatt = patt + [c]
        if len(results) == k and (len(newmdb), newpatt) <= results[0]:
            break

        topk_rec(newpatt, newmdb)


if __name__ == "__main__":
    def checkArg(arg, cond):
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
    # db = [
        # [0, 1, 2, 3, 4],
        # [1, 1, 1, 3, 4],
        # [2, 1, 2, 2, 0],
        # [1, 1, 1, 2, 2],
    # ]

    if argv["frequent"]:
        minsup = checkArg("<threshold>", lambda v: 0 < v <= len(db))
        func = frequent_rec
    elif argv["top-k"]:
        k = checkArg("<threshold>", lambda v: 0 < v)
        func = topk_rec

    if argv["--minlen"]:
        __minlen = checkArg("--minlen", lambda v: 0 < v)
    if argv["--maxlen"]:
        __maxlen = checkArg("--maxlen", lambda v: __minlen <= v)

    func([], [(i, 0) for i in xrange(len(db))])

    if argv["top-k"]:
        results.sort(key=(lambda (freq, patt): (-freq, patt)))
    for (freq, patt) in results:
        print("{} : {}".format(' '.join(str(v) for v in patt), freq))
