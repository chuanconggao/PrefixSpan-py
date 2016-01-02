#! /usr/bin/env python3

import sys
from collections import defaultdict

db = [
    [0, 1, 2, 3, 4],
    [1, 1, 1, 3, 4],
    [2, 1, 2, 2, 0],
    [1, 1, 1, 2, 2],
]

minsup = 2

#  db = []
#  with open(sys.argv[1]) as f:
    #  for line in f:
        #  db.append(line.rstrip().split(' '))

#  minsup = int(sys.argv[2])

results = []

def mine_rec(patt, mdb):
    occurs = defaultdict(list)

    for (i, stoppos) in mdb:
        seq = db[i]
        for j in range(stoppos, len(seq)):
            l = occurs[seq[j]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, j + 1))

    for (c, newmdb) in occurs.items():
        newsup = len(newmdb)

        if newsup >= minsup:
            newpatt = patt + [c]

            results.append((newpatt, len(newmdb)))
            mine_rec(newpatt, newmdb)

mine_rec([], [(i, 0) for i in range(len(db))])

print(results)
