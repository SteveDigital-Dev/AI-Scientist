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


if __name__ == "__main__":
    unittest.main()
