# AI Scientist Harness Refinement Report — 2026-06-07

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Goal: run one measured refinement cycle with a small reversible harness improvement and preserve the evidence trail.

## Benchmark Set
### Fixed benchmark
- Command: `python tests/benchmark_runner.py --start-dir tests --pattern test_*.py --trials 3 --warmup 1 --reuse-discovery`
- Metrics: pass rate, error rate, average latency, stdev

### Validation gate
- Command: `python -m unittest -v tests.test_benchmark_runner tests.test_hypothesis_record_validation tests.test_auto_research tests.test_ranking_determinism`
- Purpose: confirm no reliability regression on the focused harness suite

## Baseline (pre-change)
### Reliability / latency baseline
- Trials: 3/3 pass
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.501286 s**
- Stdev: **0.005115 s**
- Artifact: `reports/harness-refinement-2026-06-07-baseline.json`

### Quality baseline
- Focused harness validation suite: **PASS**
- Interpretation: existing artifact-persistence and validation coverage already held at 100%; this run targeted benchmark overhead reduction rather than new correctness coverage.

## Candidate Hypothesis
The benchmark suite is paying avoidable subprocess overhead in `tests/test_benchmark_runner.py`. Keep one true subprocess CLI test for end-to-end coverage, but convert the stdout/file payload parity check to an in-process `main(argv=..., stdout=...)` call. This should preserve quality while reducing benchmark latency.

## Successful Candidate
### Change
- Added `build_parser()` to `tests/benchmark_runner.py`
- Refactored `main()` to accept optional `argv` and `stdout`
- Kept one real subprocess-backed CLI test for end-to-end coverage
- Switched the payload-parity test in `tests/test_benchmark_runner.py` to the new in-process path

### Files touched
- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`

## Failed Candidates
- None in this cycle.

## Candidate Results (post-change)
### Reliability / latency benchmark
- Trials: 3/3 pass
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.285961 s**
- Stdev: **0.025080 s**
- Artifact: `reports/harness-refinement-2026-06-07-candidate.json`

### Quality / reliability gate
- `python -m unittest -v tests.test_benchmark_runner tests.test_hypothesis_record_validation tests.test_auto_research tests.test_ranking_determinism` → **PASS** (16/16)
- Observed run time: **0.373 s**

## Comparison
### Quality delta
- Harness validation result: **PASS → PASS**
- Functional coverage preserved for artifact creation and stdout/file payload parity.

### Reliability delta
- Pass rate: **100% → 100%**
- Error rate: **0% → 0%**
- Critical reliability regression: **none**

### Latency / throughput delta
- Avg latency: **0.501286 s → 0.285961 s**
- Latency change: **-42.95%**
- Relative throughput change: **+75.30%**

## Acceptance Decision
**APPLY**

Reason: the candidate produced a reproducible latency improvement on the fixed 3-trial benchmark set while preserving 100% pass rate and focused harness validation coverage.

## Report Paths
- `reports/harness-refinement-2026-06-07.md`
- `reports/harness-refinement-2026-06-07-baseline.json`
- `reports/harness-refinement-2026-06-07-candidate.json`

## Generated Artifacts
- Benchmark JSON: `reports/harness-refinement-2026-06-07-baseline.json`
- Benchmark JSON: `reports/harness-refinement-2026-06-07-candidate.json`

## Failure Traces / Blockers
- No functional blockers encountered.
- Non-blocking note: Git warned that `tests/test_benchmark_runner.py` will normalize `LF` to `CRLF` on future Windows checkout/touch.

## Next Hypothesis
Reduce residual benchmark variance by separating ultra-fast in-process timing from broader regression coverage, so nightly reports can show both a stable micro-latency signal and a broader confidence gate without conflating them.
