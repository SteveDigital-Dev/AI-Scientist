# AI Scientist Harness Refinement Report — 2026-05-12

## Scope
Nightly local harness refinement in `D:\GitHub\AI-Scientist`.

## Baseline (fixed benchmark set)
Command:
`python tests/benchmark_runner.py --start-dir tests --pattern test_auto_research.py --trials 5 --warmup 1`

Results:
- Trials: 5
- Avg latency: **0.00329414 s**
- Std dev: **0.00016533 s**
- Pass rate: **100%**
- Error rate: **0%**

## Candidate Hypothesis
Reduce per-trial overhead by discovering tests once and reloading by test IDs (`--reuse-discovery` mode) instead of re-running unittest discovery each trial.

Temporary change attempted:
- `tests/benchmark_runner.py`
  - Added test-id collection helper
  - Added `run_once_from_ids(...)`
  - Added `--reuse-discovery` flag

## Candidate Benchmark
Command:
`python tests/benchmark_runner.py --start-dir tests --pattern test_auto_research.py --trials 5 --warmup 1 --reuse-discovery`

Results:
- Trials: 5
- Avg latency: **0.00396652 s**
- Std dev: **0.00009215 s**
- Pass rate: **100%**
- Error rate: **0%**

## Comparison
- Latency delta: **+20.41% slower** (candidate vs baseline)
- Quality delta (pass rate): **no change**
- Reliability delta (error rate): **no change**

## Decision
**REJECT / REVERT** candidate.

Reason:
- Did not meet apply threshold (needed >=10% throughput/latency improvement or >=5% quality improvement).
- Reliability remained good, but performance regressed.

## Revert + Verification
- Reverted `tests/benchmark_runner.py` to original implementation.
- Verification run after revert:
  - `python tests/benchmark_runner.py --start-dir tests --pattern test_auto_research.py --trials 3 --warmup 1`
  - Pass rate: 100%, Error rate: 0%

## Diffs Touched
- `tests/benchmark_runner.py` (temporary candidate edit, then reverted)
- `reports/harness-refinement-2026-05-12.md` (new)

## Commit Status
- Not committed.
- Blocker: repository has no `.git` metadata (`fatal: not a git repository`).

## Next Hypothesis
Try a lower-risk harness optimization with clearer upside:
1. Add optional JSONL append mode to capture multiple benchmark runs in one process and reduce shell/process startup overhead in nightly orchestration.
2. Compare against current benchmark command with matched trial counts and warmup.
3. Apply only if >=10% latency/throughput gain and reliability remains unchanged.
