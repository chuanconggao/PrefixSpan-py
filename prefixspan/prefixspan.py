#! /usr/bin/env python3

from typing import *

Matches = List[Tuple[int, int]]
Pattern = List[int]
Results = List[Tuple[int, Pattern]]

Key = Callable[[Pattern, Matches], Any]
Filter = Callable[[Pattern, Matches], bool]

from collections import defaultdict
from heapq import heappop, heappush

class PrefixSpan(object):
    def __init__(self, db):
        # type: (List[List[int]]) -> None
        self._db = db

        self.minlen, self.maxlen = 1, 1000

        self._results = [] # type: Results


    # BIDE
    def _reversescan(self, patt, matches):
        # type: (List[Union[int, None]], Matches) -> bool
        def islocalclosed(previtem):
            # type: (Union[int, None]) -> bool
            closeditems = set() # type: Set[int]

            for k, match in enumerate(matches):
                i, endpos = match

                localitems = set()

                for startpos in range(endpos - 1, -1, -1):
                    item = self._db[i][startpos]

                    if item == previtem:
                        matches[k] = (i, startpos)
                        break

                    localitems.add(item)

                (closeditems.update if k == 0 else closeditems.intersection_update)(localitems)

            return len(closeditems) > 0


        matches = matches[:]

        return any(
            islocalclosed(previtem)
            for previtem in reversed(patt[:-1])
        )


    # BIDE
    def _isclosed(self, patt, matches):
        # type: (Pattern, Matches) -> bool
        # Add a pseduo item indicating the start of sequence
        # Add a pseduo item indicating the end of sequence
        return not self._reversescan(
            [None, *patt, None],
            [(i, len(self._db[i])) for i, _ in matches]
        )

    # BIDE
    def _canprune(self, patt, matches):
        # type: (Pattern, Matches) -> bool
        # Add a pseduo item indicating the start of sequence
        return self._reversescan([None, *patt], matches)


    def _scan(self, matches):
        # type: (Matches) -> Dict[int, Matches]
        alloccurs = defaultdict(list) # type: Dict[int, Matches]

        for i, pos in matches:
            seq = self._db[i]

            occurs = set() # type: Set[int]
            for j in range(pos + 1, len(seq)):
                k = seq[j]
                if k not in occurs:
                    occurs.add(k)
                    alloccurs[k].append((i, j))

        return alloccurs


    def _mine(self, func):
        # type: (Callable[[Pattern, Matches], None]) -> Results
        self._results.clear()

        func([], [(i, -1) for i in range(len(self._db))])

        return self._results


    def frequent(self, minsup, key=None, filter=None, closed=False, pruning=True):
        # type: (int, Union[None, Key], Union[None, Filter], bool, bool) -> Results

        def frequent_rec(patt, matches):
            # type: (Pattern, Matches) -> None
            if len(patt) >= self.minlen:
                if (
                        (filter is None or filter(patt, matches)) and
                        (not closed or self._isclosed(patt, matches))
                    ):
                    self._results.append((key(patt, matches), patt))

                if len(patt) == self.maxlen:
                    return

            for c, newmatches in self._scan(matches).items():
                newpatt = patt + [c]
                if pruning and (
                        key(newpatt, newmatches) < minsup or
                        closed and self._canprune(newpatt, newmatches)
                    ):
                    continue

                frequent_rec(newpatt, newmatches)


        db = self._db # Expose for key and filter
        if key is None:
            key = lambda patt, matches: len(matches)

        return self._mine(frequent_rec)


    def topk(self, k, key=None, filter=None, closed=False, pruning=True):
        # type: (int, Union[None, Key], Union[None, Filter], bool, bool) -> Results

        def topk_rec(patt, matches):
            # type: (Pattern, Matches) -> None
            if len(patt) >= self.minlen:
                if (
                        (filter is None or filter(patt, matches)) and
                        (not closed or self._isclosed(patt, matches))
                    ):
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
                if pruning:
                    if len(self._results) == k and key(newpatt, newmatches) <= self._results[0][0]:
                        break

                    if closed and self._canprune(newpatt, newmatches):
                        continue

                topk_rec(newpatt, newmatches)


        db = self._db # Expose for key and filter
        if key is None:
            key = lambda patt, matches: len(matches)

        # Sort by support in reverse, then by pattern.
        return sorted(self._mine(topk_rec), key=lambda x: (-x[0], x[1]))
