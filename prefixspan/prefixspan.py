#! /usr/bin/env python3

from .localtyping import *

class PrefixSpan(object):
    def __init__(self, db):
        # type: (List[List[int]]) -> None
        self._db = db

        self.minlen, self.maxlen = 1, 1000

        self._results = [] # type: Any


    def _mine(self, func):
        # type: (Callable[[Pattern, Matches], None]) -> Any
        self._results.clear()

        func([], [(i, -1) for i in range(len(self._db))])

        return self._results


    frequent = None # type: Callable
    topk = None # type: Callable

    defaultkey = lambda patt, matches: len(matches)
