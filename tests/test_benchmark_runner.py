import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests import benchmark_runner


ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tests" / "benchmark_runner.py"
CLI_SMOKE_PATTERN = "test_cli_smoke_fixture.py"
REUSE_DISCOVERY_PATTERN = "test_reuse_discovery_fixture.py"


class BenchmarkRunnerCliTest(unittest.TestCase):
    def test_output_writes_json_file_and_creates_parent_dirs(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "artifacts" / "benchmark.json"
            cmd = [
                sys.executable,
                str(RUNNER),
                "--start-dir",
                "tests",
                "--pattern",
                CLI_SMOKE_PATTERN,
                "--trials",
                "1",
                "--warmup",
                "0",
                "--reuse-discovery",
                "--output",
                str(output_path),
            ]

            result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue(output_path.exists())

            payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["pattern"], CLI_SMOKE_PATTERN)
            self.assertEqual(payload["pass_rate"], 1.0)

    def test_output_file_matches_stdout_payload(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = Path(tmp_dir) / "benchmark.json"
            stdout = io.StringIO()

            with mock.patch.object(sys, "argv", [str(RUNNER)]):
                exit_code = benchmark_runner.main(
                    [
                        "--start-dir",
                        "tests",
                        "--pattern",
                        CLI_SMOKE_PATTERN,
                        "--trials",
                        "1",
                        "--warmup",
                        "0",
                        "--reuse-discovery",
                        "--output",
                        str(output_path),
                    ],
                    stdout=stdout,
                )

            self.assertEqual(exit_code, 0)

            stdout_payload = json.loads(stdout.getvalue())
            file_payload = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(file_payload, stdout_payload)

    def test_output_includes_latency_summary_fields(self):
        stdout = io.StringIO()

        exit_code = benchmark_runner.main(
            [
                "--start-dir",
                "tests",
                "--pattern",
                CLI_SMOKE_PATTERN,
                "--trials",
                "1",
                "--warmup",
                "0",
                "--reuse-discovery",
            ],
            stdout=stdout,
        )

        self.assertEqual(exit_code, 0)

        payload = json.loads(stdout.getvalue())
        self.assertIn("median_seconds", payload)
        self.assertIn("min_seconds", payload)
        self.assertIn("max_seconds", payload)
        self.assertIn("p95_seconds", payload)
        self.assertEqual(payload["median_seconds"], payload["avg_seconds"])
        self.assertEqual(payload["min_seconds"], payload["avg_seconds"])
        self.assertEqual(payload["max_seconds"], payload["avg_seconds"])
        self.assertEqual(payload["p95_seconds"], payload["avg_seconds"])
        self.assertIn("throughput_trials_per_second", payload)
        self.assertEqual(payload["throughput_trials_per_second"], 1 / payload["avg_seconds"])
        self.assertEqual(payload["successful_trials"], 1)
        self.assertEqual(payload["failed_trials"], 0)

    def test_nearest_rank_percentile_uses_tail_trial(self):
        values = [0.1, 0.2, 0.3, 0.4, 0.9]

        percentile = benchmark_runner._nearest_rank_percentile(values, 95)

        self.assertEqual(percentile, 0.9)

    def test_reuse_discovery_clones_suite_for_each_trial(self):
        stdout = io.StringIO()

        exit_code = benchmark_runner.main(
            [
                "--start-dir",
                "tests",
                "--pattern",
                REUSE_DISCOVERY_PATTERN,
                "--trials",
                "3",
                "--warmup",
                "0",
                "--reuse-discovery",
            ],
            stdout=stdout,
        )

        self.assertEqual(exit_code, 0)

        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["successful_trials"], 3)
        self.assertEqual(payload["failed_trials"], 0)
        self.assertEqual(payload["pass_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
