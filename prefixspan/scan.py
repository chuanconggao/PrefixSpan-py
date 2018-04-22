#! /usr/bin/env python3

from .localtyping import *

from collections import defaultdict

def scan(db, matches):
    # type: (DB, Matches) -> Dict[int, Matches]
    alloccurs = defaultdict(list) # type: Dict[int, Matches]

    for i, pos in matches:
        seq = db[i]

        occurs = set() # type: Set[int]
        for j in range(pos + 1, len(seq)):
            k = seq[j]
            if k not in occurs:
                occurs.add(k)
                alloccurs[k].append((i, j))

    return alloccurs
