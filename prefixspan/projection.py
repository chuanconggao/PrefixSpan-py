#! /usr/bin/env python3

from collections import defaultdict

from extratools.dicttools import nextentries as unrestricted_nextentries

from .localtyping import DB, Matches, Occurs


class ProjectedMatches(list):
    """One public match and all valid internal endpoints per sequence."""

    def __init__(self, endpoints):
        self.endpoints = {
            sequence_id: tuple(sorted(positions))
            for sequence_id, positions in endpoints.items()
        }
        super().__init__(
            (sequence_id, self.endpoints[sequence_id][0])
            for sequence_id in sorted(self.endpoints)
        )


def nextentries(db: DB, matches: Matches, max_gap=None) -> Occurs:
    """Return prefix extensions, optionally limiting skipped items."""
    if max_gap is None:
        return unrestricted_nextentries(db, matches)

    if isinstance(matches, ProjectedMatches):
        endpoints = matches.endpoints.items()
    else:
        endpoints = ((sequence_id, (endpos,)) for sequence_id, endpos in matches)

    occurrences = defaultdict(lambda: defaultdict(set))

    for sequence_id, previous_positions in endpoints:
        sequence = db[sequence_id]

        for previous_position in previous_positions:
            if previous_position == -1:
                candidate_positions = range(len(sequence))
            else:
                candidate_positions = range(
                    previous_position + 1,
                    min(len(sequence), previous_position + max_gap + 2),
                )

            for position in candidate_positions:
                occurrences[sequence[position]][sequence_id].add(position)

    return {
        item: ProjectedMatches(item_endpoints)
        for item, item_endpoints in occurrences.items()
    }
