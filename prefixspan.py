#! /usr/bin/env python

from __future__ import print_function

import sys
from collections import defaultdict

#  db = [
    #  [0, 1, 2, 3, 4],
    #  [1, 1, 1, 3, 4],
    #  [2, 1, 2, 2, 0],
    #  [1, 1, 1, 2, 2],
#  ]

#  minsup = 2

db = [
    [int(v) for v in line.rstrip().split(' ')]
    for line in sys.stdin
]

minsup = int(sys.argv[1])

results = []

def mine_rec(patt, mdb):
    results.append((patt, len(mdb)))

    occurs = defaultdict(list)
    for (i, startpos) in mdb:
        seq = db[i]
        for j in xrange(startpos, len(seq)):
            l = occurs[seq[j]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, j + 1))

    for (c, newmdb) in occurs.iteritems():
        if len(newmdb) >= minsup:
            mine_rec(patt + [c], newmdb)

mine_rec([], [(i, 0) for i in xrange(len(db))])

print(results)
