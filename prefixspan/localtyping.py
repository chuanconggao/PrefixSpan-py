#! /usr/bin/env python3

from typing import *

DB = List[List[int]]

Matches = List[Tuple[int, int]]
Occurs = Dict[int, Matches]

Pattern = List[int]
Results = Optional[List[Tuple[int, Pattern]]]

Key = Callable[[Pattern, Matches], int]
Filter = Callable[[Pattern, Matches], bool]

Callback = Callable[[Pattern, Matches], None]
