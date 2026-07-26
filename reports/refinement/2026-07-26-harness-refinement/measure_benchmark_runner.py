import argparse
import importlib.util
import io
import json
import statistics
import tempfile
import time
import traceback
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CLI_SMOKE_PATTERN = "test_cli_smoke_fixture.py"


def load_module(module_path: Path):
    spec = importlib.util.spec_from_file_location("bench_target", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_cli_smoke(module) -> None:
    stdout = io.StringIO()
    exit_code = module.main(
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
    payload = json.loads(stdout.getvalue())
    assert exit_code == 0, payload
    assert payload["successful_trials"] == 1, payload
    assert payload["failed_trials"] == 0, payload


def run_default_loader_isolation(module) -> None:
    stdout = io.StringIO()
    original_top_level_dir = unittest.defaultTestLoader._top_level_dir
    try:
        unittest.defaultTestLoader._top_level_dir = str(Path(tempfile.gettempdir()) / "unrelated-root")
        exit_code = module.main(
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

    payload = json.loads(stdout.getvalue())
    assert exit_code == 0, payload
    assert payload["failed_trials"] == 0, payload


def _run_temp_failure_fixture(module) -> dict:
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
            )
            + "\n",
            encoding="utf-8",
        )

        stdout = io.StringIO()
        exit_code = module.main(
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
        payload = json.loads(stdout.getvalue())
        return {"exit_code": exit_code, "payload": payload}


def run_repeated_temp_fixture(module) -> None:
    first = _run_temp_failure_fixture(module)
    second = _run_temp_failure_fixture(module)

    for result in (first, second):
        payload = result["payload"]
        assert result["exit_code"] == 1, payload
        assert payload["failed_trials"] == 1, payload
        assert payload["failure_count"] == 1, payload
        assert "AssertionError" in payload["first_failure"]["message"], payload


def run_trial(module) -> tuple[bool, list[dict[str, str]]]:
    failures = []
    scenarios = [
        ("cli_smoke", run_cli_smoke),
        ("default_loader_isolation", run_default_loader_isolation),
        ("repeated_temp_fixture", run_repeated_temp_fixture),
    ]

    for scenario_name, scenario in scenarios:
        try:
            scenario(module)
        except Exception as exc:  # pragma: no cover - artifact script
            failures.append(
                {
                    "scenario": scenario_name,
                    "message": f"{type(exc).__name__}: {exc}",
                    "traceback": traceback.format_exc(),
                }
            )

    return len(failures) == 0, failures


def build_summary(trials: list[dict]) -> dict:
    seconds = [trial["seconds"] for trial in trials]
    successful_trials = sum(1 for trial in trials if trial["success"])
    failed_trials = len(trials) - successful_trials
    pass_rate = successful_trials / len(trials)
    error_rate = 1.0 - pass_rate

    return {
        "successful_trials": successful_trials,
        "failed_trials": failed_trials,
        "pass_rate": pass_rate,
        "error_rate": error_rate,
        "avg_seconds": statistics.mean(seconds),
        "median_seconds": statistics.median(seconds),
        "min_seconds": min(seconds),
        "max_seconds": max(seconds),
        "throughput_trials_per_second": len(trials) / sum(seconds),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--module-path", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--failure-trace", required=True)
    parser.add_argument("--trials", type=int, default=5)
    args = parser.parse_args()

    module = load_module(Path(args.module_path))

    trials = []
    failure_traces = []
    for i in range(max(args.trials, 1)):
        start = time.perf_counter()
        success, failures = run_trial(module)
        seconds = time.perf_counter() - start
        trial = {
            "trial": i + 1,
            "success": success,
            "seconds": seconds,
        }
        if failures:
            trial["failure_summaries"] = [
                {
                    "scenario": failure["scenario"],
                    "message": failure["message"],
                }
                for failure in failures
            ]
            failure_traces.extend(
                [
                    {
                        "trial": i + 1,
                        "scenario": failure["scenario"],
                        "message": failure["message"],
                        "traceback": failure["traceback"],
                    }
                    for failure in failures
                ]
            )
        trials.append(trial)

    payload = {
        "label": args.label,
        "module_path": str(Path(args.module_path).resolve()),
        "benchmark_set": [
            "cli_smoke",
            "default_loader_isolation",
            "repeated_temp_fixture",
        ],
        "trials": trials,
        "summary": build_summary(trials),
    }

    output_path = Path(args.output)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    trace_path = Path(args.failure_trace)
    if failure_traces:
        rendered_traces = []
        for trace in failure_traces:
            rendered_traces.append(
                "\n".join(
                    [
                        f"trial: {trace['trial']}",
                        f"scenario: {trace['scenario']}",
                        f"message: {trace['message']}",
                        trace["traceback"].rstrip(),
                    ]
                )
            )
        trace_path.write_text("\n\n".join(rendered_traces) + "\n", encoding="utf-8")
    else:
        trace_path.write_text("No failures recorded.\n", encoding="utf-8")

    print(json.dumps(payload, indent=2))
    return 0 if payload["summary"]["failed_trials"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
