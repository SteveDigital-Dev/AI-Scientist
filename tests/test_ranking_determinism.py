"""
Test deterministic ranking of hypothesis records with ties.

This test validates that rank_hypotheses produces consistent ordering
when multiple records have the same score but different timestamps/names.
"""

import unittest
from ai_scientist.auto_research import rank_hypotheses


class RankingDeterminismTest(unittest.TestCase):
    """Ensure rank_hypotheses is deterministic with ties."""

    def test_ties_resolved_by_timestamp_ascending(self):
        """When scores are equal, records sorted by timestamp ascending (earliest first)."""
        records = [
            {"name": "idea_3", "score": 8.0, "timestamp": "2026-05-31T10:00:00Z"},
            {"name": "idea_1", "score": 8.0, "timestamp": "2026-05-29T10:00:00Z"},
            {"name": "idea_2", "score": 8.0, "timestamp": "2026-05-30T10:00:00Z"},
        ]
        
        ranked = rank_hypotheses(records)
        self.assertEqual([r["name"] for r in ranked], ["idea_1", "idea_2", "idea_3"])

    def test_ties_resolved_by_name_ascending_after_timestamp(self):
        """When both score and timestamp are equal, sort by name ascending (lexicographic)."""
        records = [
            {"name": "idea_z", "score": 7.0, "timestamp": "2026-05-31T10:00:00Z"},
            {"name": "idea_a", "score": 7.0, "timestamp": "2026-05-31T10:00:00Z"},
            {"name": "idea_m", "score": 7.0, "timestamp": "2026-05-31T10:00:00Z"},
        ]
        
        ranked = rank_hypotheses(records)
        self.assertEqual([r["name"] for r in ranked], ["idea_a", "idea_m", "idea_z"])

    def test_missing_score_treated_as_negative_infinity(self):
        """Records without scores appear after all records with actual scores."""
        records = [
            {"name": "idea_with_score", "score": 9.0, "timestamp": "2026-05-31T10:00:00Z"},
            {"name": "idea_no_score", "timestamp": "2026-05-30T10:00:00Z"},
        ]
        
        ranked = rank_hypotheses(records)
        self.assertEqual(ranked[0]["name"], "idea_with_score")
        self.assertEqual(ranked[1]["name"], "idea_no_score")

    def test_empty_input_returns_empty_list(self):
        """Ranking empty input should return empty list, not crash."""
        records = []
        ranked = rank_hypotheses(records)
        self.assertEqual(ranked, [])


if __name__ == "__main__":
    unittest.main()
