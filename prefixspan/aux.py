#! /usr/bin/env python3

from typing import *

T = TypeVar('T')

def sorteddiff(a: Iterable[T], b: Iterable[T], key=lambda v: v) -> Iterable[T]:
    # Assume a and b are sorted, where set(a) >= set(b)
    # Output equals to sorted(set(a) - set(b))

    x, y = iter(a), iter(b)

    m: Union[T, None] = None
    n: Union[T, None] = None

    while True:
        m, n = next(x, None), n or next(y, None)
        if n is None:
            break

        if key(m) == key(n):
            n = None
        else:
            yield m

    while m is not None:
        yield m

        m = next(x, None)


def issubseq(a: Iterable[T], b: Iterable[T]) -> bool:
    x, y = iter(a), iter(b)

    m: Union[T, None] = None
    n: Union[T, None] = None

    while True:
        m, n = m or next(x, None), next(y, None)
        if m is None or n is None:
            break

        if m == n:
            m = None

    return m is None
