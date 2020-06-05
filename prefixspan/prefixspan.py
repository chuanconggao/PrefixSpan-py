#! /usr/bin/env python3

from .localtyping import List, Callable, Matches, Pattern, Any


class PrefixSpan(object):
    def __init__(self, db: List[List[int]]):
        self._db = db

        self.minlen, self.maxlen = 1, 1000

        self._results: Any = []

    def _mine(self, func: Callable[[Pattern, Matches], None]) -> Any:
        self._results.clear()

        func([], [(i, -1) for i in range(len(self._db))])

        return self._results

    frequent: Callable = None
    topk: Callable = None

    @staticmethod
    def defaultkey(patt, matches):
        return len(matches)
