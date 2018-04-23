#! /usr/bin/env python3

from .localtyping import *

from heapq import heappush, heappushpop

from .scan import scan
from .closed import isclosed, canprune

class PrefixSpan(object):
    def __init__(self, db):
        # type: (List[List[int]]) -> None
        self._db = db

        self.minlen, self.maxlen = 1, 1000

        self._results = [] # type: Results


    def _mine(self, func):
        # type: (Callable[[Pattern, Matches], None]) -> Results
        self._results.clear()

        func([], [(i, -1) for i in range(len(self._db))])

        return self._results


    def frequent(
            self, minsup, closed=False,
            key=None, bound=None,
            filter=None
        ):
        # type: (int, bool, Union[None, Key], Union[None, Key], Union[None, Filter]) -> Results
        def canpass(sup):
            # type: (int) -> bool
            return sup < minsup


        def verify(patt, matches):
            # type: (Pattern, Matches) -> None
            sup = key(patt, matches)
            if canpass(sup):
                return

            if (not closed or isclosed(self._db, patt, matches)) and (filter is None or filter(patt, matches)):
                self._results.append((sup, patt))


        def frequent_rec(patt, matches):
            # type: (Pattern, Matches) -> None
            if len(patt) >= self.minlen:
                verify(patt, matches)

                if len(patt) == self.maxlen:
                    return

            for newitem, newmatches in scan(db, matches).items():
                newpatt = patt + [newitem]
                if canpass(bound(newpatt, newmatches)) or closed and canprune(db, newpatt, newmatches):
                    continue

                frequent_rec(newpatt, newmatches)


        db = self._db # Expose for key and filter to access
        if key is None:
            key = bound = lambda patt, matches: len(matches)

        return self._mine(frequent_rec)


    def topk(
            self, k, closed=False,
            key=None, bound=None,
            filter=None
        ):
        # type: (int, bool, Union[None, Key], Union[None, Key], Union[None, Filter]) -> Results
        def canpass(sup):
            # type: (int) -> bool
            return len(self._results) == k and sup <= self._results[0][0]


        def verify(patt, matches):
            # type: (Pattern, Matches) -> None
            sup = key(patt, matches)
            if canpass(sup):
                return

            if (not closed or isclosed(self._db, patt, matches)) and (filter is None or filter(patt, matches)):
                (heappush if len(self._results) < k else heappushpop)(self._results, (sup, patt))


        def topk_rec(patt, matches):
            # type: (Pattern, Matches) -> None
            if len(patt) >= self.minlen:
                verify(patt, matches)

                if len(patt) == self.maxlen:
                    return

            for newitem, newmatches in sorted(
                    scan(db, matches).items(),
                    key=lambda x: key(patt + [x[0]], x[1]),
                    reverse=True
                ):
                newpatt = patt + [newitem]

                if canpass(bound(newpatt, newmatches)):
                    break
                if closed and canprune(db, newpatt, newmatches):
                    continue

                topk_rec(newpatt, newmatches)


        db = self._db # Expose for key and filter to access
        if key is None:
            key = bound = lambda patt, matches: len(matches)

        # Sort by support in reverse, then by pattern.
        return sorted(self._mine(topk_rec), key=lambda x: (-x[0], x[1]))
