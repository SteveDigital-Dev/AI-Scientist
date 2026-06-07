import argparse
import io
import json
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


def run_once(start_dir: str, pattern: str, discovered_suite=None) -> tuple[bool, float]:
    start = time.perf_counter()
    if discovered_suite is None:
        suite = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern=pattern)
    else:
        suite = discovered_suite
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    seconds = time.perf_counter() - start
    success = result.wasSuccessful()
    return success, seconds


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
        ok, sec = run_once(args.start_dir, args.pattern, discovered_suite)
        trials.append({"trial": i + 1, "success": ok, "seconds": sec})

    pass_rate = sum(1 for t in trials if t["success"]) / len(trials)
    error_rate = 1.0 - pass_rate
    avg_seconds = statistics.mean(t["seconds"] for t in trials)
    stdev_seconds = statistics.pstdev(t["seconds"] for t in trials)

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
        "avg_seconds": avg_seconds,
        "stdev_seconds": stdev_seconds,
        "pass_rate": pass_rate,
        "error_rate": error_rate,
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
