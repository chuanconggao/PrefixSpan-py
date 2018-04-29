#! /usr/bin/env python3

from .prefixspan import PrefixSpan

from .frequent import PrefixSpan_frequent
from .topk import PrefixSpan_topk

PrefixSpan.frequent = PrefixSpan_frequent
PrefixSpan.topk = PrefixSpan_topk
