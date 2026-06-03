# AI Scientist Harness Refinement Report — 2026-05-31

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Benchmark target: `tests/test_auto_research.py`
- Baseline command: `python tests/benchmark_runner.py --start-dir tests --pattern test_auto_research.py --trials 5 --warmup 1 --reuse-discovery`

## Baseline (pre-change)
- Trials: 5/5 pass
- Pass rate: 100%
- Error rate: 0%
- Avg latency: **0.007366 s**
- Stdev: 0.003018 s

## Candidate Hypothesis
When discovery reuse is enabled, avoid per-trial `deepcopy` by reusing the discovered suite in-place with `TestSuite._cleanup=False` recursively set. This should reduce harness overhead without changing test semantics.

## Candidate Results
- Trials: 5/5 pass
- Pass rate: 100%
- Error rate: 0%
- Avg latency: **0.006238 s**
- Stdev: 0.004804 s

## Reproducibility Check
Additional A/B strategy benchmark (20 trials each, same process):
- Baseline strategy (deepcopy): **0.010395 s avg**, pass rate 100%
- Candidate strategy (in-place suite reuse): **0.007932 s avg**, pass rate 100%
- Latency improvement: **23.69% faster**

## Comparison
- Quality delta: 0% (no quality score change measured)
- Reliability delta: no regression (100% -> 100%)
- Latency delta (primary 5-trial run): **15.31% faster**

## Decision
**APPLY**

Reason: Meets threshold via latency improvement >=10% and no critical reliability/error regression.

## Diffs Touched
- `tests/benchmark_runner.py`
  - Removed `copy.deepcopy` trial cloning path
  - Added recursive suite cleanup disable helper
  - Reused discovered suite in-place when `--reuse-discovery` is enabled

## Validation Gate
- `python -m unittest tests/test_auto_research.py` -> **PASS** (3/3 tests)

## Commit Status
- [blocked] Repo has no `.git` metadata (`fatal: not a git repository`), so required commit step is unavailable.
- Fallback plan: once `.git` is restored/initialized, commit this single-file change with message:
  - `harness: reuse discovered unittest suite to cut benchmark overhead`

## Next Hypothesis
Profile `TextTestRunner` setup overhead and test stream handling to evaluate whether a reusable runner/stream path can yield another >=10% latency gain without reducing result fidelity.
