#! /usr/bin/env python3

from .localtyping import DB, Pattern, Matches, List, Occurs

from extratools.seqtools import issubseqwithgap
from extratools.sortedtools import sorteddiff


def isgenerator(db: DB, patt: Pattern, matches: Matches, occursstack: List[Occurs]):
    # Try to remove the last item
    if (
        len(db) if len(patt) < 2
        else len(occursstack[len(patt) - 2][patt[-2]])
    ) == len(matches):
        return False

    for i in range(len(patt) - 1, 0, -1):
        # Try to remove the (i-1)-th item
        item = patt[i]

        # occursstack[0] is for patt == []
        prevoccurs, occurs = occursstack[i - 1][item], occursstack[i][item]
        if len(prevoccurs) == len(occurs) or all(
            not issubseqwithgap(patt[i + 1:], db[k][pos + 1:])
            for k, pos in sorteddiff(prevoccurs, occurs, key=lambda x: x[0])
        ):
            return False

    return True


def cangeneratorprune(db: DB, patt: Pattern, matches: Matches, occursstack: List[Occurs]) -> bool:
    for i in range(len(patt) - 1, 0, -1):
        # Try to remove the (i-1)-th item
        item = patt[i]

        # occursstack[0] is for patt == []
        if occursstack[i - 1][item] == occursstack[i][item]:
            return True

    return False
