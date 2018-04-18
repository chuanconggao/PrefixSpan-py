#! /usr/bin/env python3

from typing import *
Matches = List[Tuple[int, int]]
Pattern = List[int]
Results = List[Tuple[int, Pattern]]
Key = Callable[[Pattern, Matches], Any]
Filter = Callable[[Pattern, Matches], bool]

import sys
from collections import defaultdict
from heapq import heappop, heappush

class PrefixSpan(object):
    def __init__(self, db):
        # type: (List[List[int]]) -> None
        self._db = db

        self.minlen, self.maxlen = 1, sys.maxsize

        self._results = [] # type: Results


    def _mine(self, func):
        # type: (Callable[[Pattern, Matches], None]) -> Results
        self._results.clear()

        func([], [(i, 0) for i in range(len(self._db))])

        return self._results


    def _scan(self, matches):
        # type: (Matches) -> Dict[int, Matches]
        alloccurs = defaultdict(list) # type: Dict[int, Matches]

        for i, pos in matches:
            seq = self._db[i]

            occurs = set() # type: Set[int]
            for j in range(pos, len(seq)):
                k = seq[j]
                if k not in occurs:
                    occurs.add(k)
                    alloccurs[k].append((i, j + 1))

        return alloccurs


    def frequent(self, minsup, key=None, filter=None):
        # type: (int, Union[None, Key], Union[None, Filter]) -> Results

        def frequent_rec(patt, matches):
            # type: (Pattern, Matches) -> None
            if len(patt) >= self.minlen:
                if filter is None or filter(patt, matches):
                    self._results.append((key(patt, matches), patt))

                if len(patt) == self.maxlen:
                    return

            for c, newmatches in self._scan(matches).items():
                newpatt = patt + [c]
                if key(newpatt, newmatches) >= minsup:
                    frequent_rec(newpatt, newmatches)


        db = self._db # Expose for key and filter
        if key is None:
            key = lambda patt, matches: len(matches)

        return self._mine(frequent_rec)


    def topk(self, k, key=None, filter=None):
        # type: (int, Union[None, Key], Union[None, Filter]) -> Results

        def topk_rec(patt, matches):
            # type: (Pattern, Matches) -> None
            if len(patt) >= self.minlen:
                if filter is None or filter(patt, matches):
                    heappush(self._results, (key(patt, matches), patt))
                    if len(self._results) > k:
                        heappop(self._results)

                if len(patt) == self.maxlen:
                    return

            for c, newmatches in sorted(
                    self._scan(matches).items(),
                    key=lambda x: key(patt + [x[0]], x[1]),
                    reverse=True
                ):
                newpatt = patt + [c]
                if len(self._results) == k and key(newpatt, newmatches) <= self._results[0][0]:
                    break

                topk_rec(newpatt, newmatches)


        db = self._db # Expose for key and filter
        if key is None:
            key = lambda patt, matches: len(matches)

        return sorted(self._mine(topk_rec), key=lambda x: -x[0])
