#! /usr/bin/env python3

from .localtyping import Pattern, Matches, Optional, Key, Filter, Callback, Results, List, Occurs

from heapq import heappush, heappushpop

from extratools.dicttools import nextentries

from .prefixspan import PrefixSpan
from .closed import isclosed, canclosedprune
from .generator import isgenerator, cangeneratorprune


def PrefixSpan_topk(
    self: PrefixSpan, k: int, closed=False, generator=False,
    key: Optional[Key] = None, bound: Optional[Key] = None,
    filter: Optional[Filter] = None, callback: Optional[Callback] = None
) -> Results:
    if generator:
        occursstack: List[Occurs] = []

    def canpass(sup: int) -> bool:
        return len(self._results) == k and sup <= self._results[0][0]

    def verify(patt: Pattern, matches: Matches):
        sup = key(patt, matches)
        if canpass(sup):
            return

        if (filter is None or filter(patt, matches)) and (
            (not closed or isclosed(self._db, patt, matches)) and
            (not generator or isgenerator(
                self._db, patt, matches, occursstack))
        ):
            (heappush if len(self._results) < k else heappushpop)(
                self._results, (sup, patt, matches))

    def topk_rec(patt: Pattern, matches: Matches):
        if len(patt) >= self.minlen:
            verify(patt, matches)

            if len(patt) == self.maxlen:
                return

        occurs = nextentries(self._db, matches)
        if generator:
            occursstack.append(occurs)

        for newitem, newmatches in sorted(
            occurs.items(),
            key=lambda x: key(patt + [x[0]], x[1]),
            reverse=True
        ):
            newpatt = patt + [newitem]

            if canpass(bound(newpatt, newmatches)):
                break

            if (
                closed and canclosedprune(self._db, newpatt, newmatches) or
                generator and cangeneratorprune(
                    self._db, newpatt, newmatches, occursstack)
            ):
                continue

            topk_rec(newpatt, newmatches)

        if generator:
            occursstack.pop()

    if key is None:
        key = bound = PrefixSpan.defaultkey

    # Sort by support in reverse, then by pattern.
    results = sorted(self._mine(topk_rec), key=lambda x: (-x[0], x[1]))

    if callback:
        for _, patt, matches in results:
            callback(patt, matches)

        return None

    return [(sup, patt) for sup, patt, _ in results]
