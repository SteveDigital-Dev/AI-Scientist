import argparse
import copy
import io
import json
import math
import statistics
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _disable_suite_cleanup(node) -> None:
    if isinstance(node, unittest.TestSuite):
        # Preserve tests after each run so a discovered suite can be reused in place.
        node._cleanup = False
        for child in node:
            _disable_suite_cleanup(child)


def _nearest_rank_percentile(values: list[float], percentile: float) -> float:
    if not values:
        raise ValueError("values must not be empty")
    if percentile <= 0:
        return min(values)
    if percentile >= 100:
        return max(values)

    ordered = sorted(values)
    rank = max(1, math.ceil((percentile / 100) * len(ordered)))
    return ordered[rank - 1]


def _summarize_outcome(case: unittest.case.TestCase, detail: str) -> dict[str, str]:
    lines = [line.strip() for line in detail.splitlines() if line.strip()]
    headline = lines[-1] if lines else ""
    for line in reversed(lines):
        if "Error" in line or "Exception" in line:
            headline = line
            break
    return {
        "test": case.id(),
        "message": headline,
    }


def _collect_failure_summaries(result: unittest.TestResult) -> list[dict[str, str]]:
    summaries = []
    for case, detail in list(result.failures) + list(result.errors):
        summaries.append(_summarize_outcome(case, detail))
    return summaries


def _build_failure_rollup(trials: list[dict[str, object]]) -> dict[str, object]:
    failed_tests = []
    first_failure = None
    failure_count = 0

    for trial in trials:
        for summary in trial.get("failure_summaries", []):
            failure_count += 1
            if first_failure is None:
                first_failure = summary
            test_id = summary["test"]
            if test_id not in failed_tests:
                failed_tests.append(test_id)

    return {
        "failed_tests": failed_tests,
        "first_failure": first_failure,
        "failure_count": failure_count,
    }


def run_once(start_dir: str, pattern: str, discovered_suite=None) -> tuple[bool, float, list[dict[str, str]]]:
    start = time.perf_counter()
    if discovered_suite is None:
        suite = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern=pattern)
    else:
        # Isolate each trial from test-instance mutations while still avoiding re-discovery.
        suite = copy.deepcopy(discovered_suite)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    seconds = time.perf_counter() - start
    success = result.wasSuccessful()
    failure_summaries = _collect_failure_summaries(result)
    return success, seconds, failure_summaries


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run lightweight in-process benchmark trials.")
    parser.add_argument("--start-dir", default="tests", help="unittest discover start directory")
    parser.add_argument("--pattern", default="test_auto_research.py", help="unittest discover pattern")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--warmup", type=int, default=1)
    parser.add_argument(
        "--reuse-discovery",
        dest="reuse_discovery",
        action="store_true",
        default=True,
        help="discover tests once, then deepcopy suite each trial (default: enabled)",
    )
    parser.add_argument(
        "--no-reuse-discovery",
        dest="reuse_discovery",
        action="store_false",
        help="re-discover tests for every trial",
    )
    parser.add_argument(
        "--output",
        help="optional path to write the JSON benchmark payload",
    )
    return parser


def main(argv: list[str] | None = None, stdout=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    discovered_suite = None
    if args.reuse_discovery:
        discovered_suite = unittest.defaultTestLoader.discover(start_dir=args.start_dir, pattern=args.pattern)
        _disable_suite_cleanup(discovered_suite)

    for _ in range(max(args.warmup, 0)):
        run_once(args.start_dir, args.pattern, discovered_suite)

    trials = []
    for i in range(max(args.trials, 1)):
        ok, sec, failure_summaries = run_once(args.start_dir, args.pattern, discovered_suite)
        trial = {"trial": i + 1, "success": ok, "seconds": sec}
        if failure_summaries:
            trial["failure_summaries"] = failure_summaries
        trials.append(trial)

    pass_rate = sum(1 for t in trials if t["success"]) / len(trials)
    error_rate = 1.0 - pass_rate
    successful_trials = sum(1 for t in trials if t["success"])
    failed_trials = len(trials) - successful_trials
    seconds = [t["seconds"] for t in trials]
    avg_seconds = statistics.mean(seconds)
    median_seconds = statistics.median(seconds)
    stdev_seconds = statistics.pstdev(seconds)
    min_seconds = min(seconds)
    max_seconds = max(seconds)
    p95_seconds = _nearest_rank_percentile(seconds, 95)
    throughput_trials_per_second = len(trials) / sum(seconds)
    failure_rollup = _build_failure_rollup(trials)

    command = [
        "python",
        "tests/benchmark_runner.py",
        "--start-dir",
        args.start_dir,
        "--pattern",
        args.pattern,
        "--trials",
        str(args.trials),
        "--warmup",
        str(args.warmup),
        "--reuse-discovery" if args.reuse_discovery else "--no-reuse-discovery",
    ]

    payload = {
        "command": " ".join(command),
        "start_dir": args.start_dir,
        "pattern": args.pattern,
        "reuse_discovery": args.reuse_discovery,
        "trials": trials,
        "successful_trials": successful_trials,
        "failed_trials": failed_trials,
        "avg_seconds": avg_seconds,
        "median_seconds": median_seconds,
        "stdev_seconds": stdev_seconds,
        "min_seconds": min_seconds,
        "max_seconds": max_seconds,
        "p95_seconds": p95_seconds,
        "throughput_trials_per_second": throughput_trials_per_second,
        "pass_rate": pass_rate,
        "error_rate": error_rate,
        "failed_tests": failure_rollup["failed_tests"],
        "first_failure": failure_rollup["first_failure"],
        "failure_count": failure_rollup["failure_count"],
        "summary": {
            "reliability": {
                "successful_trials": successful_trials,
                "failed_trials": failed_trials,
                "pass_rate": pass_rate,
                "error_rate": error_rate,
            },
            "failures": failure_rollup,
            "latency_seconds": {
                "avg": avg_seconds,
                "median": median_seconds,
                "stdev": stdev_seconds,
                "min": min_seconds,
                "max": max_seconds,
                "p95": p95_seconds,
            },
            "throughput": {
                "trials_per_second": throughput_trials_per_second,
            },
        },
    }
    rendered = json.dumps(payload, indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")

    print(rendered, file=stdout or sys.stdout)
    return 0 if pass_rate == 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
