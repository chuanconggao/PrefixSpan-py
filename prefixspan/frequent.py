#! /usr/bin/env python3

from .localtyping import *

from .prefixspan import PrefixSpan
from .scan import scan
from .closed import isclosed, canprune

def PrefixSpan_frequent(
        self, minsup, closed=False,
        key=None, bound=None,
        filter=None
    ):
    # type: (PrefixSpan, int, bool, Union[None, Key], Union[None, Key], Union[None, Filter]) -> Results
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

        for newitem, newmatches in scan(self._db, matches).items():
            newpatt = patt + [newitem]
            if canpass(bound(newpatt, newmatches)) or closed and canprune(self._db, newpatt, newmatches):
                continue

            frequent_rec(newpatt, newmatches)


    if key is None:
        key = bound = PrefixSpan.defaultkey

    return self._mine(frequent_rec)
