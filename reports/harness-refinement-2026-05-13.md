# Harness Refinement Report — 2026-05-13

## Scope
Nightly harness refinement loop in `D:\GitHub\AI-Scientist`.

## Benchmark Setup
- Command (baseline): `python tests/benchmark_runner.py --start-dir tests --pattern test_auto_research.py --trials 5 --warmup 1`
- Command (candidate): `python tests/benchmark_runner.py --start-dir tests --pattern test_auto_research.py --trials 5 --warmup 1 --reuse-discovery`
- Fixed benchmark set: `tests/test_auto_research.py`
- Trials: 5 (>=3 required)

## Baseline Metrics
- Avg latency: **0.0079627 s**
- Stddev: 0.0005075 s
- Pass rate: **100%**
- Error rate: **0%**

## Candidate Hypothesis
Pre-discover tests once and reload by test IDs (`--reuse-discovery`) to reduce per-trial discovery overhead.

## Candidate Metrics
- Avg latency: **0.0099486 s**
- Stddev: 0.0005181 s
- Pass rate: **100%**
- Error rate: **0%**

## Delta (Candidate vs Baseline)
- Latency: **+24.94% slower** (regression)
- Throughput proxy (1/latency): **-19.96%**
- Reliability: no regression (pass/error unchanged)

## Decision
**REJECT / REVERT**

Acceptance threshold was not met (needed >=10% latency/throughput improvement or >=5% quality gain with no critical reliability regression). Candidate caused a clear performance regression.

## Diffs Touched
- `tests/benchmark_runner.py` (candidate attempted, then fully reverted to prior content)

## Commit Status
- No commit created.
- Blocker: repository has no `.git` metadata (`fatal: not a git repository`).

## Next Hypothesis
Try optimizing benchmark output overhead instead of test loading path:
1. Add optional compact output mode (single-line JSON / reduced serialization work).
2. Benchmark `python -m unittest` subprocess vs in-process runner under same fixed test set.
3. If stable, test small retry/backoff or timeout handling improvements in harness execution path.
