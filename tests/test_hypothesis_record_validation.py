import unittest

from ai_scientist.auto_research import build_hypothesis_record


class HypothesisRecordValidationTest(unittest.TestCase):
    def test_missing_name_raises_value_error(self):
        idea = {
            "Title": "Missing Name",
            "Experiment": "Run with unnamed idea.",
            "novel": True,
        }

        with self.assertRaises(ValueError):
            build_hypothesis_record(
                idea=idea,
                success=True,
                score=7.0,
                run_path="results/run_1",
                timestamp="2026-06-04T05:00:00Z",
            )

    def test_missing_experiment_raises_value_error(self):
        idea = {
            "Name": "missing_experiment",
            "Title": "Missing Experiment",
            "novel": False,
        }

        with self.assertRaises(ValueError):
            build_hypothesis_record(
                idea=idea,
                success=False,
                score=3.5,
                run_path="results/run_2",
                timestamp="2026-06-04T05:00:00Z",
            )

    def test_non_numeric_score_raises_value_error(self):
        idea = {
            "Name": "bad_score",
            "Title": "Bad Score",
            "Experiment": "Try malformed score handling.",
        }

        with self.assertRaises(ValueError):
            build_hypothesis_record(
                idea=idea,
                success=True,
                score="not-a-number",
                run_path="results/run_3",
                timestamp="2026-06-04T05:00:00Z",
            )

    def test_blank_run_path_raises_value_error(self):
        idea = {
            "Name": "blank_path",
            "Title": "Blank Path",
            "Experiment": "Ensure persisted path metadata is required.",
        }

        with self.assertRaises(ValueError):
            build_hypothesis_record(
                idea=idea,
                success=True,
                score=1.0,
                run_path="   ",
                timestamp="2026-06-04T05:00:00Z",
            )


if __name__ == "__main__":
    unittest.main()
