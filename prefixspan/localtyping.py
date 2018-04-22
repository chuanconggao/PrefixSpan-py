#! /usr/bin/env python3

from typing import *

DB = List[List[int]]
Matches = List[Tuple[int, int]]
Pattern = List[int]
Results = List[Tuple[int, Pattern]]

Key = Callable[[Pattern, Matches], Any]
Filter = Callable[[Pattern, Matches], bool]
