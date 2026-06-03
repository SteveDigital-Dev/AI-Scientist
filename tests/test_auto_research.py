import json
import tempfile
import unittest
from pathlib import Path

from ai_scientist.auto_research import (
    append_hypothesis_record,
    build_hypothesis_record,
    rank_hypotheses,
)


class AutoResearchHelpersTest(unittest.TestCase):
    def test_build_hypothesis_record_maps_expected_fields(self):
        idea = {
            "Name": "adaptive_sampler",
            "Title": "Adaptive Sampler for Better Generalization",
            "Experiment": "Adjust batch sampling strategy using uncertainty signals.",
            "novel": True,
            "Interestingness": 8,
            "Feasibility": 7,
            "Novelty": 9,
        }

        record = build_hypothesis_record(
            idea=idea,
            success=True,
            score=7.5,
            run_path="results/nanoGPT/20260407_adaptive_sampler",
            timestamp="2026-04-07T01:23:45Z",
        )

        self.assertEqual(record["name"], "adaptive_sampler")
        self.assertEqual(record["title"], "Adaptive Sampler for Better Generalization")
        self.assertEqual(record["hypothesis"], idea["Experiment"])
        self.assertTrue(record["novel"])
        self.assertEqual(record["score"], 7.5)
        self.assertTrue(record["success"])
        self.assertEqual(record["run_path"], "results/nanoGPT/20260407_adaptive_sampler")
        self.assertEqual(record["timestamp"], "2026-04-07T01:23:45Z")

    def test_rank_hypotheses_orders_by_score_desc(self):
        records = [
            {"name": "idea_low", "score": 3.0},
            {"name": "idea_top", "score": 9.0},
            {"name": "idea_mid", "score": 6.0},
        ]

        ranked = rank_hypotheses(records)
        self.assertEqual([r["name"] for r in ranked], ["idea_top", "idea_mid", "idea_low"])

    def test_append_hypothesis_record_writes_jsonl(self):
        record = {"name": "idea_1", "score": 5.0}

        with tempfile.TemporaryDirectory() as tmp_dir:
            jsonl_path = Path(tmp_dir) / "auto_research_hypotheses.jsonl"
            append_hypothesis_record(jsonl_path, record)

            lines = jsonl_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(json.loads(lines[0]), record)


if __name__ == "__main__":
    unittest.main()
