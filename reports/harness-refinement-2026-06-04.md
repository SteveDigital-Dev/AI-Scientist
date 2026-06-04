# AI Scientist Harness Refinement Report — 2026-06-04

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Primary goal: improve measurable harness quality/reliability with a small reversible change.
- Local agent CLI check:
  - `opencode --help` → available
  - `pi --help` → available
  - `pi -p ...` refinement attempt → blocked by provider connection error, so final refinement used direct local code/test loop.

## Benchmark Set
### Reliability / latency benchmark
- Command: `python tests/benchmark_runner.py --start-dir tests --pattern test_*.py --trials 3 --warmup 1 --reuse-discovery`
- Metrics: pass rate, error rate, average latency, stdev

### Quality benchmark
- Command: `python -m unittest tests.test_hypothesis_record_validation`
- Trials: 3
- Focus: malformed hypothesis metadata should fail fast instead of silently producing partially invalid records.

## Baseline (pre-change)
### Reliability / latency baseline
- Trials: 3/3 pass
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.005076 s**
- Stdev: **0.000222 s**

### Quality baseline
- Trials: 0/3 pass
- Pass rate: **0%**
- Error rate: **100%**
- Avg latency: **0.168590 s**
- Stdev: **0.018927 s**
- Failure details:
  - missing `Name` did not raise
  - missing `Experiment` did not raise
  - blank `run_path` did not raise
  - non-numeric `score` already raised correctly
- Test-level score: **1/4 passing**

## Candidate Hypothesis
Add minimal input validation to `build_hypothesis_record` so malformed idea metadata is rejected immediately. This should improve harness quality/reproducibility by preventing silent propagation of invalid records while keeping the change small and reversible.

## Candidate Change
- Added `_require_non_empty_string(...)` helper in `ai_scientist/auto_research.py`
- Enforced required non-empty values for:
  - `idea["Name"]`
  - `idea["Experiment"]`
  - `run_path`
- Added regression coverage in `tests/test_hypothesis_record_validation.py`

## Candidate Results (post-change)
### Reliability / latency benchmark
- Trials: 3/3 pass
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.005497 s**
- Stdev: **0.000397 s**

### Quality benchmark
- Trials: 3/3 pass
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.189443 s**
- Stdev: **0.037786 s**
- Test-level score: **4/4 passing**

## Comparison
### Quality delta
- Validation pass rate: **0% → 100%**
- Test-level score: **1/4 → 4/4** (**+300%** on passing checks; **+75 percentage points** absolute)

### Reliability delta
- Full-suite pass rate: **100% → 100%**
- Full-suite error rate: **0% → 0%**
- No critical regression observed.

### Latency delta
- Full-suite latency: **0.005076 s → 0.005497 s** (**8.29% slower**)
- This does **not** meet the throughput-improvement acceptance path, but it stays below the rejection threshold because the accepted improvement is quality-based and reliability did not regress.

## Decision
**APPLY**

Reason: quality improvement exceeded the required threshold by a wide margin, and the existing suite remained 100% reliable. The small latency cost is acceptable for the added fail-fast validation behavior.

## Diffs Touched
- `ai_scientist/auto_research.py`
- `tests/test_hypothesis_record_validation.py`

## Validation Gate
- `python -m unittest -v tests.test_hypothesis_record_validation tests.test_auto_research tests.test_ranking_determinism` → **PASS** (11/11)
- `python tests/benchmark_runner.py --start-dir tests --pattern test_*.py --trials 3 --warmup 1 --reuse-discovery` → **PASS** (3/3)

## Next Hypothesis
Validate optional numeric metadata (`Interestingness`, `Feasibility`, `Novelty`) for type/range normalization so nightly runs can reject malformed scoring payloads before ranking/persistence.
