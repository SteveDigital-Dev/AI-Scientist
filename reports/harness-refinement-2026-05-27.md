# AI Scientist Harness Refinement Report - 2026-05-27

## Scope
Nightly local harness refinement in `D:\GitHub\AI-Scientist`.

## Baseline (fixed benchmark, >=3 trials)
Command:
`python tests/benchmark_runner.py --trials 5 --warmup 1`

Results:
- Pass rate: 100% (5/5)
- Error rate: 0.0%
- Avg latency: **0.00423434 s**
- Std dev: 0.00019105 s

## Candidate Hypothesis
Cache discovered test IDs and rebuild suite with `loadTestsFromNames` each trial to reduce deepcopy overhead.

Temporary change:
- File touched: `tests/benchmark_runner.py`
- Added `--reuse-test-ids` path and test-id extraction helper.

## Candidate Benchmark (>=3 trials)
Command:
`python tests/benchmark_runner.py --trials 5 --warmup 1 --reuse-test-ids`

Results:
- Pass rate: 100% (5/5)
- Error rate: 0.0%
- Avg latency: **0.00403770 s**
- Std dev: 0.00009543 s

## Comparison
- Latency delta: **-4.64%** (faster)
- Quality/reliability: no regression (100% pass, 0% error both sides)

## Decision
**REJECT / REVERT**

Reason: Improvement did not meet apply threshold (requires >=10% throughput/latency gain or >=5% quality gain).

## Reversion
- Reverted `tests/benchmark_runner.py` to original implementation.
- Verification run after revert:
  - `python tests/benchmark_runner.py --trials 3 --warmup 1`
  - Pass rate 100%, avg latency 0.00427647 s.

## Diff Footprint
- Temporary diff created and then reverted in:
  - `tests/benchmark_runner.py`
- Net persisted code changes: **none**.

## Commit Status
No commit created.

Blocker: `D:\GitHub\AI-Scientist` currently has no `.git` metadata (`fatal: not a git repository`).

## Next Hypothesis
Try reducing runner overhead instead of suite construction overhead, e.g. pre-create `TextTestRunner` and reuse stream buffers across trials, then re-benchmark with same thresholds.
