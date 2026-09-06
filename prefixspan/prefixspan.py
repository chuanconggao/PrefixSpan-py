#! /usr/bin/env python3

from numbers import Integral

from .localtyping import List, Callable, Matches, Pattern, Any


class PrefixSpan(object):
    def __init__(self, db: List[List[int]], max_gap=None):
        self._db = db

        self.minlen, self.maxlen = 1, 1000
        self.max_gap = max_gap

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

    @property
    def max_gap(self):
        return self._max_gap

    @max_gap.setter
    def max_gap(self, value):
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, Integral) or value < 0
        ):
            raise ValueError("max_gap must be None or a non-negative integer")

        self._max_gap = None if value is None else int(value)

    def _validate_gap_options(self, closed: bool, generator: bool):
        if self.max_gap is not None and (closed or generator):
            raise ValueError(
                "closed and generator mining are not supported with max_gap"
            )
