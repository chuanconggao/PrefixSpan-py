#! /usr/bin/env python3

from .localtyping import Results, Optional, Key, Callback, Filter, Pattern, Matches, List, Occurs

from extratools.dicttools import nextentries

from .prefixspan import PrefixSpan
from .closed import isclosed, canclosedprune
from .generator import isgenerator, cangeneratorprune


def PrefixSpan_frequent(
    self, minsup: int, closed=False, generator=False,
    key: Optional[Key] = None, bound: Optional[Key] = None,
    filter: Optional[Filter] = None, callback: Optional[Callback] = None
) -> Results:
    if generator:
        occursstack: List[Occurs] = []

    def canpass(sup: int) -> bool:
        return sup < minsup

    def verify(patt: Pattern, matches: Matches):
        sup = key(patt, matches)
        if canpass(sup):
            return

        if (filter is None or filter(patt, matches)) and (
            (not closed or isclosed(self._db, patt, matches)) and
            (not generator or isgenerator(
                self._db, patt, matches, occursstack))
        ):
            if callback:
                callback(patt, matches)
            else:
                self._results.append((sup, patt))

    def frequent_rec(patt: Pattern, matches: Pattern):
        if len(patt) >= self.minlen:
            verify(patt, matches)

            if len(patt) == self.maxlen:
                return

        occurs = nextentries(self._db, matches)
        if generator:
            occursstack.append(occurs)

        for newitem, newmatches in occurs.items():
            newpatt = patt + [newitem]

            if canpass(bound(newpatt, newmatches)) or\
                (closed and canclosedprune(self._db, newpatt, newmatches)) or\
                    (generator and cangeneratorprune(self._db, newpatt, newmatches, occursstack)):
                continue

            frequent_rec(newpatt, newmatches)

        if generator:
            occursstack.pop()

    if key is None:
        key = bound = PrefixSpan.defaultkey

    results = self._mine(frequent_rec)

    return None if callback else results
