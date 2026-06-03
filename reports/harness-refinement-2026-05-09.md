# AI Scientist Harness Refinement Report

Date: 2026-05-09 01:00 ET
Repo: `D:\GitHub\AI-Scientist`
Run type: nightly cron harness refinement

## Scope and blockers
- Requested tools (`opencode` / `pi cli`) were not available/configured in this repo.
- Fallback used: local Python harness reliability benchmark via unit test target `tests/test_auto_research.py`.

## Benchmark definition
Command (3 trials each condition):
`python -m unittest discover -s tests -p test_auto_research.py`

Metrics:
- Quality/reliability proxy: pass rate (% successful runs)
- Error rate: failed runs / total
- Throughput proxy: wall-clock seconds per trial (lower is better)

## Baseline (before change)
Trials:
- t1: exit 1, 0.346s
- t2: exit 1, 0.239s
- t3: exit 1, 0.223s

Aggregate:
- pass rate: 0/3 = **0%**
- error rate: 3/3 = **100%**
- avg latency: **0.269s**

Failure mode:
- `ModuleNotFoundError: No module named 'ai_scientist.auto_research'`

## Candidate improvement
Hypothesis:
- Adding missing `ai_scientist/auto_research.py` with tested helper functions will remove import failures and restore harness reliability.

Change made:
- Added `ai_scientist/auto_research.py` implementing:
  - `build_hypothesis_record(...)`
  - `rank_hypotheses(...)`
  - `append_hypothesis_record(...)`

## Candidate results (after change)
Trials:
- t1: exit 0, 0.383s
- t2: exit 0, 0.255s
- t3: exit 0, 0.245s

Aggregate:
- pass rate: 3/3 = **100%**
- error rate: 0/3 = **0%**
- avg latency: **0.294s**

## Comparison and decision
Deltas (candidate vs baseline):
- pass rate: **+100 percentage points** (0% -> 100%)
- error rate: **-100 percentage points** (100% -> 0%)
- avg latency: **+9.3% slower** (0.269s -> 0.294s)

Decision:
- **APPLY** candidate.
- Acceptance criterion met via major quality/reliability improvement (>> 5%) with no critical reliability regression (reliability improved dramatically).

## Files touched
- Added: `ai_scientist/auto_research.py`
- Added: `reports/harness-refinement-2026-05-09.md`

## Commit status
- Could not commit: no `.git` directory detected under `D:\GitHub\AI-Scientist`.
- Fallback plan: once repo git metadata is restored/initialized, commit this change as:
  - `fix(harness): add missing auto_research helpers to restore benchmark reliability`

## Next hypothesis
- Add a micro-benchmark script that records structured JSON metrics for nightly runs (pass/error/latency trendline) to support automated regression gating beyond one test module.
