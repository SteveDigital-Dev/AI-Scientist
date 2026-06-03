# AI Scientist Harness Refinement Report

Date: 2026-05-20 01:00 ET
Repo: `D:\GitHub\AI-Scientist`
Run type: nightly cron harness refinement

## Scope and blockers
- Requested tools (`opencode` / `pi cli`) were not available/configured in this repo path.
- Fallback used: local Python benchmark harness on `tests/test_auto_research.py`.
- Git metadata is still missing in this directory (no `.git`), so commit step is blocked.

## Benchmark definition
Fixed benchmark set:
- `tests/test_auto_research.py`

Baseline command (5 trials, 1 warmup):
- `python tests/benchmark_runner.py --start-dir tests --pattern test_auto_research.py --trials 5 --warmup 1 --reuse-discovery`

Candidate command (5 trials, 1 warmup):
- `python tests/benchmark_runner.py --start-dir tests --pattern test_auto_research.py --trials 5 --warmup 1 --reuse-discovery --direct-result`

Metrics:
- Reliability: pass rate, error rate
- Throughput/latency: average seconds per trial (lower is better)

## Baseline metrics
Trials (seconds):
- 0.0031255001
- 0.0028989001
- 0.0027717000
- 0.0028120001
- 0.0027340000

Aggregate:
- pass rate: **100%**
- error rate: **0%**
- avg latency: **0.0028684200s**
- stdev: **0.0001397325s**

## Candidate hypothesis
Hypothesis:
- Bypass `TextTestRunner` and execute the suite directly with `unittest.TestResult` to reduce runner overhead.

## Candidate metrics
Trials (seconds):
- 0.0032865000
- 0.0031116001
- 0.0031141000
- 0.0030657999
- 0.0032946999

Aggregate:
- pass rate: **100%**
- error rate: **0%**
- avg latency: **0.0031745400s**
- stdev: **0.0000963455s**

## Comparison and decision
Deltas (candidate vs baseline):
- quality/reliability: no change (100% pass, 0% error)
- avg latency: **+10.67% slower** (regression)

Decision:
- **REVERT** candidate.
- Candidate fails acceptance criteria (did not improve quality by >=5% or latency/throughput by >=10%).

## Diffs touched
- Temporary edit and revert: `tests/benchmark_runner.py`
- Final persisted artifact: `reports/harness-refinement-2026-05-20.md`

## Commit status
- Not committed (blocked: no `.git` directory).

## Next hypothesis
- Test a reusable prebuilt suite strategy that avoids `copy.deepcopy` per trial while preserving correctness (e.g., explicit suite regeneration from cached test IDs).