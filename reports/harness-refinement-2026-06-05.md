# AI Scientist Harness Refinement Report — 2026-06-05

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Goal: improve measurable harness quality/reliability with one small reversible change.
- Local agent CLI check:
  - `opencode --help` → available
  - `opencode run ...` → blocked by local plugin/runtime error: `Cannot find module '../../lib/skills-core.js'` from `C:\Users\Steve Digital\.config\opencode\plugin\superpowers.js`
  - Fallback used: direct local code/test iteration

## Benchmark Set
### Reliability / latency benchmark
- Command: `python tests/benchmark_runner.py --start-dir tests --pattern test_*.py --trials 3 --warmup 1 --reuse-discovery`
- Metrics: pass rate, error rate, average latency, stdev

### Quality benchmark
- Fixed cases exercised 3 times against `build_hypothesis_record(...)`:
  1. reject string `Interestingness`
  2. reject out-of-range `Feasibility=11`
  3. reject out-of-range `Novelty=0`
  4. accept and preserve valid float `Interestingness=7.5`
- Metric: case pass rate per trial

## Baseline (pre-change)
### Reliability / latency baseline
- Trials: 3/3 pass
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.005233 s**
- Stdev: **0.000025 s**

### Quality baseline
- Trials: 3/3 completed
- Per-trial result: **1/4 passing cases**
- Pass rate: **25%**
- Error rate: **75%**
- Failures:
  - string `Interestingness` was silently accepted
  - `Feasibility=11` was silently accepted
  - `Novelty=0` was silently accepted

## Candidate Hypothesis
Normalize optional numeric idea metadata (`Interestingness`, `Feasibility`, `Novelty`) to floats and reject malformed or out-of-range values early. This should improve harness quality/reproducibility by preventing invalid scoring metadata from being persisted or ranked.

## Candidate Change
- Added `_normalize_optional_score(...)` in `ai_scientist/auto_research.py`
- Enforced numeric type and inclusive `1..10` range for:
  - `idea["Interestingness"]`
  - `idea["Feasibility"]`
  - `idea["Novelty"]`
- Normalized valid optional numeric metadata to `float`
- Added regression coverage in `tests/test_hypothesis_record_validation.py`

## Candidate Results (post-change)
### Reliability / latency benchmark
- Trials: 3/3 pass
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.006154 s**
- Stdev: **0.000740 s**

### Quality benchmark
- Trials: 3/3 completed
- Per-trial result: **4/4 passing cases**
- Pass rate: **100%**
- Error rate: **0%**

## Comparison
### Quality delta
- Case pass rate: **25% → 100%**
- Absolute improvement: **+75 percentage points**
- Relative improvement: **+300%**

### Reliability delta
- Full-suite pass rate: **100% → 100%**
- Full-suite error rate: **0% → 0%**
- No critical reliability regression observed.

### Latency delta
- Full-suite latency: **0.005233 s → 0.006154 s**
- Change: **17.62% slower**
- This does not qualify on throughput, but the candidate clears the quality acceptance path and preserves reliability.

## Decision
**APPLY**

Reason: quality improvement exceeded the required threshold by a wide margin, and the benchmark suite remained fully reliable. The latency increase is measurable but small in absolute terms and acceptable for the added validation.

## Diffs Touched
- `ai_scientist/auto_research.py`
- `tests/test_hypothesis_record_validation.py`
- `reports/harness-refinement-2026-06-05.md`

## Validation Gate
- `python -m unittest -v tests.test_hypothesis_record_validation tests.test_auto_research tests.test_ranking_determinism` → **PASS** (14/14)
- `python tests/benchmark_runner.py --start-dir tests --pattern test_*.py --trials 3 --warmup 1 --reuse-discovery` → **PASS** (3/3)

## Next Hypothesis
Reduce benchmark variance and overhead by splitting discovery/setup cost from execution timing in `tests/benchmark_runner.py`, then compare whether the tighter signal makes nightly apply/reject decisions more reliable.