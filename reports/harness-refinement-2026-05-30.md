# AI Scientist Harness Refinement Report — 2026-05-30

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Benchmark target: `tests/test_auto_research.py`
- Command: `python tests/benchmark_runner.py --start-dir tests --pattern test_auto_research.py --trials 5 --warmup 1 --reuse-discovery`

## Baseline (pre-change)
- Trials: 5/5 pass
- Pass rate: 100%
- Error rate: 0%
- Avg latency: **0.002948 s**
- Stdev: 0.000120 s

## Candidate Hypothesis
Replace `copy.deepcopy(discovered_suite)` with test-id flatten/rebuild per trial to reduce copy overhead and improve reliability around non-deepcopy-safe suites.

## Candidate Results
- Trials: 5/5 pass
- Pass rate: 100%
- Error rate: 0%
- Avg latency: **0.004581 s**
- Stdev: 0.000077 s

## Comparison
- Quality delta: 0% (no score change measured)
- Reliability delta: no regression (100% -> 100%)
- Latency delta: **-55.40% throughput equivalent** (candidate is slower)

## Decision
**REJECT / REVERT**

Reason: does not meet apply thresholds (needs >=5% quality gain or >=10% throughput/latency improvement). Candidate regressed latency materially.

## Diffs Touched
- `tests/benchmark_runner.py` (temporary candidate edit)
- Reverted to original implementation in same run (no intended net code change).

## Notes / Blockers
- Repo currently has no `.git` directory (`fatal: not a git repository`), so commit workflow is unavailable.

## Next Hypothesis
Try targeted optimization that avoids full `deepcopy` cost while preserving current fast path, e.g. a guarded fallback strategy:
- keep `deepcopy` as primary path
- fallback to rediscovery only on copy failure
- benchmark mixed success/failure synthetic suites to validate reliability gains without latency regression.
