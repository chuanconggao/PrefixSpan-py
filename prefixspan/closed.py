#! /usr/bin/env python3

from .localtyping import Optional, Set, Matches, DB, Pattern, List


def __reversescan(db: DB, patt: List[Optional[int]], matches: Matches):
    def islocalclosed(previtem: Optional[int]) -> bool:
        closeditems: Set[int] = set()

        for k, (i, endpos) in enumerate(matches):
            localitems = set()

            for startpos in range(endpos - 1, -1, -1):
                item = db[i][startpos]

                if item == previtem:
                    matches[k] = (i, startpos)
                    break

                localitems.add(item)

            (closeditems.update if k == 0
             else closeditems.intersection_update)(localitems)

        return len(closeditems) > 0

    return any(islocalclosed(previtem) for previtem in reversed(patt[:-1]))


def __forwardscan(db, matches):
    # type: (DB, Matches) -> bool
    closeditems = set() # type: Set[int]

    for k, (i, endpos) in enumerate(matches):
        localitems = set()

        for startpos in range(endpos + 1, len(db[i])):
            item = db[i][startpos]
            localitems.add(item)

        (closeditems.update if k == 0 else closeditems.intersection_update)(localitems)

    return len(closeditems) > 0


def isclosed(db: DB, patt: Pattern, matches: Matches) -> bool:
    # Add a pseduo item indicating the start of sequence
    # Add a pseduo item indicating the end of sequence
    return not __reversescan(
        db,
        [None, *patt, None],
        [(i, len(db[i])) for i, _ in matches]
    ) and not __forwardscan(db, matches)


def canclosedprune(db: DB, patt: Pattern, matches: Matches) -> bool:
    # Add a pseduo item indicating the start of sequence
    return __reversescan(db, [None, *patt], matches[:])
