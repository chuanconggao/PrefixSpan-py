#! /usr/bin/env python3

from collections import defaultdict

db = [
    [0, 1, 2, 3, 4],
    [1, 1, 1, 3, 4],
    [2, 1, 2, 2, 0],
    [1, 1, 1, 2, 2],
]

minsup = 2

results = []

def mine_rec(patt, mdb):
    def localOccurs(mdb):
        occurs = defaultdict(list)

        for (i, stoppos) in mdb:
            seq = db[i]
            for j in range(stoppos, len(seq)):
                l = occurs[seq[j]]
                if len(l) == 0 or l[-1][0] != i:
                    l.append((i, j + 1))

        return occurs

    for (c, newmdb) in localOccurs(mdb).items():
        newsup = len(newmdb)

        if newsup >= minsup:
            newpatt = patt + [c]

            results.append((newpatt, [i for (i, stoppos) in newmdb]))
            mine_rec(newpatt, newmdb)

mine_rec([], [(i, 0) for i in range(len(db))])

print(results)
