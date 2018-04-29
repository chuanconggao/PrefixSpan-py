#! /usr/bin/env python3

from .localtyping import *

from collections import defaultdict

def scan(db, matches):
    # type: (DB, Matches) -> Occurs
    occurs = defaultdict(list) # type: Occurs

    for i, lastpos in matches:
        seq = db[i]

        for pos in range(lastpos + 1, len(seq)):
            l = occurs[seq[pos]]
            if len(l) == 0 or l[-1][0] != i:
                l.append((i, pos))

    return occurs
