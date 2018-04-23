#! /usr/bin/env python3

from .localtyping import *

from collections import defaultdict

def scan(db, matches):
    # type: (DB, Matches) -> Dict[int, Matches]
    alloccurs = defaultdict(list) # type: Dict[int, Matches]

    for i, lastpos in matches:
        seq = db[i]

        occurs = set() # type: Set[int]
        for pos in range(lastpos + 1, len(seq)):
            item = seq[pos]
            if item not in occurs:
                occurs.add(item)
                alloccurs[item].append((i, pos))

    return alloccurs
