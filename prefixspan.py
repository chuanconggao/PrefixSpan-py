#! /usr/bin/env python

"""
Usage:
    prefixspan.py (frequent | top-k) <threshold>
"""

from __future__ import print_function

import sys
from collections import defaultdict
from heapq import heappop, heappush

from docopt import docopt

results = []

def frequent_rec(patt, mdb):
    results.append((len(mdb), patt))

    occurs = defaultdict(list)
    for (i, startpos) in mdb:
        seq = db[i]
        for j in xrange(startpos, len(seq)):
            l = occurs[seq[j]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, j + 1))

    for (c, newmdb) in occurs.iteritems():
        if len(newmdb) >= minsup:
            frequent_rec(patt + [c], newmdb)

def topk_rec(patt, mdb):
    heappush(results, (len(mdb), patt))
    if len(results) > k:
        heappop(results)

    occurs = defaultdict(list)
    for (i, startpos) in mdb:
        seq = db[i]
        for j in xrange(startpos, len(seq)):
            l = occurs[seq[j]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, j + 1))

    for (c, newmdb) in sorted(occurs.iteritems(), key=(lambda (c, newmdb): len(newmdb)), reverse=True):
        if len(results) == k and len(newmdb) <= results[0][0]:
            break

        topk_rec(patt + [c], newmdb)

if __name__ == "__main__":
    argv = docopt(__doc__)

    # db = [
        # [int(v) for v in line.rstrip().split(' ')]
        # for line in sys.stdin
    # ]

    db = [
        [0, 1, 2, 3, 4],
        [1, 1, 1, 3, 4],
        [2, 1, 2, 2, 0],
        [1, 1, 1, 2, 2],
    ]

    if argv["frequent"]:
        minsup = int(argv["<threshold>"])
        f = frequent_rec
    elif argv["top-k"]:
        k = int(argv["<threshold>"])
        f = topk_rec

    f([], [(i, 0) for i in xrange(len(db))])

    if argv["top-k"]:
        results.sort(key=(lambda (freq, patt): (-freq, patt)))
    for (freq, patt) in results:
        print("{}: {}".format(patt, freq))
