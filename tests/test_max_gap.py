import unittest

from prefixspan import PrefixSpan


class MaxGapTests(unittest.TestCase):
    def mine(self, db, max_gap, minsup=1, minlen=2, maxlen=3):
        ps = PrefixSpan(db, max_gap=max_gap)
        ps.minlen = minlen
        ps.maxlen = maxlen
        return {tuple(pattern): support for support, pattern in ps.frequent(minsup)}

    def test_none_preserves_unrestricted_subsequences(self):
        patterns = self.mine([[1, 0, 2]], max_gap=None, maxlen=2)
        self.assertEqual(patterns[(1, 2)], 1)

    def test_default_constructor_preserves_existing_results(self):
        db = [
            [0, 1, 2, 3, 4],
            [1, 1, 1, 3, 4],
            [2, 1, 2, 2, 0],
            [1, 1, 1, 2, 2],
        ]
        implicit = PrefixSpan(db).frequent(2)
        explicit = PrefixSpan(db, max_gap=None).frequent(2)
        self.assertEqual(implicit, explicit)

    def test_zero_mines_only_contiguous_patterns(self):
        patterns = self.mine([[1, 0, 2]], max_gap=0, maxlen=2)
        self.assertNotIn((1, 2), patterns)
        self.assertEqual(patterns[(1, 0)], 1)
        self.assertEqual(patterns[(0, 2)], 1)

    def test_positive_gap_bounds_skipped_items(self):
        patterns = self.mine([[1, 0, 2, 0, 3]], max_gap=1, maxlen=2)
        self.assertEqual(patterns[(1, 2)], 1)
        self.assertNotIn((1, 3), patterns)

    def test_later_occurrence_can_form_contiguous_pattern(self):
        patterns = self.mine([[1, 0, 1, 2], [1, 2]], max_gap=0, minsup=2, maxlen=2)
        self.assertEqual(patterns[(1, 2)], 2)

    def test_multiple_embeddings_count_once_per_sequence(self):
        patterns = self.mine([[1, 2, 1, 2]], max_gap=0, maxlen=2)
        self.assertEqual(patterns[(1, 2)], 1)

    def test_topk_uses_bounded_support(self):
        ps = PrefixSpan([[1, 0, 2], [1, 2], [1, 2]], max_gap=0)
        ps.minlen = ps.maxlen = 2
        self.assertEqual(ps.topk(1), [(2, [1, 2])])

    def test_callback_receives_one_match_per_sequence(self):
        ps = PrefixSpan([[1, 2, 1, 2]], max_gap=0)
        ps.minlen = ps.maxlen = 2
        observed = {}

        def callback(pattern, matches):
            observed[tuple(pattern)] = list(matches)

        ps.frequent(1, callback=callback)
        self.assertEqual(observed[(1, 2)], [(0, 1)])

    def test_custom_weighted_key_counts_each_sequence_once(self):
        weights = [5, 2]
        ps = PrefixSpan([[1, 2, 1, 2], [1, 2]], max_gap=0)
        ps.minlen = ps.maxlen = 2
        key = lambda pattern, matches: sum(weights[i] for i, _ in matches)
        self.assertEqual(ps.frequent(7, key=key), [(7, [1, 2])])
        self.assertEqual(ps.topk(1, key=key), [(7, [1, 2])])

    def test_max_gap_assignment_is_validated(self):
        ps = PrefixSpan([[1]])

        for invalid in (-1, 1.5, True, "1"):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    ps.max_gap = invalid

    def test_closed_and_generator_are_rejected_with_bounded_gap(self):
        ps = PrefixSpan([[1, 2]], max_gap=0)

        with self.assertRaises(ValueError):
            ps.frequent(1, closed=True)
        with self.assertRaises(ValueError):
            ps.topk(1, generator=True)


if __name__ == "__main__":
    unittest.main()
