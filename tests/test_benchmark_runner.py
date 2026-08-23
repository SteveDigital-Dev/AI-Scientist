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
            self.assertEqual(payload["schema_version"], benchmark_runner.SCHEMA_VERSION)
            self.assertIn("benchmark_config_digest", payload)
            self.assertIn("result_digest", payload)
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
        self.assertEqual(payload["schema_version"], benchmark_runner.SCHEMA_VERSION)
        self.assertEqual(
            payload["benchmark_config_digest"],
            benchmark_runner._build_benchmark_config_digest(
                schema_version=benchmark_runner.SCHEMA_VERSION,
                start_dir="tests",
                pattern=CLI_SMOKE_PATTERN,
                trials=1,
                warmup=0,
                reuse_discovery=True,
            ),
        )
        digest_payload = dict(payload)
        digest_payload.pop("result_digest")
        digest_payload["summary"] = dict(payload["summary"])
        digest_payload["summary"]["metadata"] = dict(payload["summary"]["metadata"])
        digest_payload["summary"]["metadata"].pop("result_digest")
        self.assertEqual(
            payload["result_digest"],
            benchmark_runner._build_result_digest(digest_payload),
        )
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
        self.assertEqual(payload["failed_tests"], [])
        self.assertEqual(payload["failed_test_counts"], {})
        self.assertEqual(payload["failed_test_rates"], {})
        self.assertIsNone(payload["first_failure"])
        self.assertEqual(payload["failure_count"], 0)
        self.assertIn("summary", payload)
        self.assertEqual(payload["summary"]["metadata"]["schema_version"], payload["schema_version"])
        self.assertEqual(
            payload["summary"]["metadata"]["benchmark_config_digest"],
            payload["benchmark_config_digest"],
        )
        self.assertEqual(payload["summary"]["metadata"]["result_digest"], payload["result_digest"])
        self.assertEqual(payload["summary"]["reliability"]["successful_trials"], 1)
        self.assertEqual(payload["summary"]["reliability"]["failed_trials"], 0)
        self.assertEqual(payload["summary"]["reliability"]["pass_rate"], payload["pass_rate"])
        self.assertEqual(payload["summary"]["reliability"]["error_rate"], payload["error_rate"])
        self.assertEqual(payload["summary"]["failures"]["failed_tests"], payload["failed_tests"])
        self.assertEqual(payload["summary"]["failures"]["failed_test_counts"], payload["failed_test_counts"])
        self.assertEqual(payload["summary"]["failures"]["failed_test_rates"], payload["failed_test_rates"])
        self.assertEqual(payload["summary"]["failures"]["first_failure"], payload["first_failure"])
        self.assertEqual(payload["summary"]["failures"]["failure_count"], payload["failure_count"])
        self.assertEqual(payload["summary"]["latency_seconds"]["avg"], payload["avg_seconds"])
        self.assertEqual(payload["summary"]["latency_seconds"]["median"], payload["median_seconds"])
        self.assertEqual(payload["summary"]["latency_seconds"]["stdev"], payload["stdev_seconds"])
        self.assertEqual(payload["summary"]["latency_seconds"]["min"], payload["min_seconds"])
        self.assertEqual(payload["summary"]["latency_seconds"]["max"], payload["max_seconds"])
        self.assertEqual(payload["summary"]["latency_seconds"]["p95"], payload["p95_seconds"])
        self.assertEqual(
            payload["summary"]["throughput"]["trials_per_second"],
            payload["throughput_trials_per_second"],
        )

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

    def test_failed_trials_include_failure_summaries(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            fixture_dir = Path(tmp_dir) / "failure_fixture"
            fixture_dir.mkdir()
            fixture_path = fixture_dir / "test_failure_fixture.py"
            fixture_path.write_text(
                "\n".join(
                    [
                        "import unittest",
                        "",
                        "",
                        "class FailureFixtureTest(unittest.TestCase):",
                        "    def test_expected_failure_signal(self):",
                        '        self.assertEqual("baseline", "candidate")',
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            stdout = io.StringIO()
            exit_code = benchmark_runner.main(
                [
                    "--start-dir",
                    str(fixture_dir),
                    "--pattern",
                    "test_failure_fixture.py",
                    "--trials",
                    "1",
                    "--warmup",
                    "0",
                    "--reuse-discovery",
                ],
                stdout=stdout,
            )

            self.assertEqual(exit_code, 1)

            payload = json.loads(stdout.getvalue())
            self.assertEqual(payload["schema_version"], benchmark_runner.SCHEMA_VERSION)
            self.assertIn("benchmark_config_digest", payload)
            self.assertIn("result_digest", payload)
            self.assertEqual(payload["failed_trials"], 1)
            self.assertEqual(payload["trials"][0]["success"], False)
            self.assertIn("failure_summaries", payload["trials"][0])
            self.assertEqual(len(payload["trials"][0]["failure_summaries"]), 1)
            failure_summary = payload["trials"][0]["failure_summaries"][0]
            self.assertEqual(
                failure_summary["test"],
                "test_failure_fixture.FailureFixtureTest.test_expected_failure_signal",
            )
            self.assertIn(
                "AssertionError",
                failure_summary["message"],
            )
            self.assertEqual(payload["failed_tests"], [failure_summary["test"]])
            self.assertEqual(payload["failed_test_counts"], {failure_summary["test"]: 1})
            self.assertEqual(payload["failed_test_rates"], {failure_summary["test"]: 1.0})
            self.assertEqual(payload["first_failure"], failure_summary)
            self.assertEqual(payload["failure_count"], 1)
            self.assertEqual(payload["summary"]["metadata"]["schema_version"], payload["schema_version"])
            self.assertEqual(
                payload["summary"]["metadata"]["benchmark_config_digest"],
                payload["benchmark_config_digest"],
            )
            self.assertEqual(payload["summary"]["metadata"]["result_digest"], payload["result_digest"])
            self.assertEqual(payload["summary"]["failures"]["failed_tests"], payload["failed_tests"])
            self.assertEqual(payload["summary"]["failures"]["failed_test_counts"], payload["failed_test_counts"])
            self.assertEqual(payload["summary"]["failures"]["failed_test_rates"], payload["failed_test_rates"])
            self.assertEqual(payload["summary"]["failures"]["first_failure"], payload["first_failure"])
            self.assertEqual(payload["summary"]["failures"]["failure_count"], payload["failure_count"])

    def test_failed_test_rates_reflect_partial_repeated_failures(self):
        trials = [
            {"trial": 1, "failure_summaries": [{"test": "pkg.TestCase.test_flaky", "message": "AssertionError"}]},
            {"trial": 2},
            {"trial": 3, "failure_summaries": [{"test": "pkg.TestCase.test_flaky", "message": "AssertionError"}]},
            {"trial": 4},
        ]

        failure_rollup = benchmark_runner._build_failure_rollup(trials)

        self.assertEqual(failure_rollup["failed_tests"], ["pkg.TestCase.test_flaky"])
        self.assertEqual(failure_rollup["failed_test_counts"], {"pkg.TestCase.test_flaky": 2})
        self.assertEqual(failure_rollup["failed_test_rates"], {"pkg.TestCase.test_flaky": 0.5})
        self.assertEqual(failure_rollup["failure_count"], 2)

    def test_repeated_temp_fixture_runs_do_not_leak_test_modules(self):
        for _ in range(2):
            with tempfile.TemporaryDirectory() as tmp_dir:
                fixture_dir = Path(tmp_dir) / "failure_fixture"
                fixture_dir.mkdir()
                fixture_path = fixture_dir / "test_failure_fixture.py"
                fixture_path.write_text(
                    "\n".join(
                        [
                            "import unittest",
                            "",
                            "",
                            "class FailureFixtureTest(unittest.TestCase):",
                            "    def test_expected_failure_signal(self):",
                            '        self.assertEqual("baseline", "candidate")',
                            "",
                        ]
                    ),
                    encoding="utf-8",
                )

                stdout = io.StringIO()
                exit_code = benchmark_runner.main(
                    [
                        "--start-dir",
                        str(fixture_dir),
                        "--pattern",
                        "test_failure_fixture.py",
                        "--trials",
                        "1",
                        "--warmup",
                        "0",
                        "--reuse-discovery",
                    ],
                    stdout=stdout,
                )

                self.assertEqual(exit_code, 1)
                payload = json.loads(stdout.getvalue())
                self.assertEqual(payload["failed_trials"], 1)
                self.assertEqual(payload["failure_count"], 1)
                self.assertIn("AssertionError", payload["first_failure"]["message"])

    def test_main_ignores_default_loader_top_level_dir_leak(self):
        stdout = io.StringIO()
        original_top_level_dir = unittest.defaultTestLoader._top_level_dir

        try:
            unittest.defaultTestLoader._top_level_dir = str(Path(tempfile.gettempdir()) / "unrelated-root")
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
        finally:
            unittest.defaultTestLoader._top_level_dir = original_top_level_dir

        self.assertEqual(exit_code, 0)
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["successful_trials"], 1)
        self.assertEqual(payload["failed_trials"], 0)


if __name__ == "__main__":
    unittest.main()
