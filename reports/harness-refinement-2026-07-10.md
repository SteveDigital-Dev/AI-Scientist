# AI Scientist Harness Refinement Report - 2026-07-10

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Goal: run one measured refinement cycle and preserve the full evidence trail.

## Benchmark Set
### Fixed benchmark
- Command: `python tests/benchmark_runner.py --start-dir tests --pattern test_benchmark_runner.py --trials 7 --warmup 1 --reuse-discovery`
- Metrics: pass rate, error rate, average latency, median latency, min/max latency, p95 latency, stdev

### Validation gate
- Command: `python -m unittest -v tests.test_benchmark_runner tests.test_cli_smoke_fixture tests.test_hypothesis_record_validation tests.test_auto_research tests.test_ranking_determinism`
- Purpose: verify the broader harness suite still passes after the candidate change

## Baseline (pre-change)
### Reliability / latency baseline
- Trials: 7/7 pass
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.440156 s**
- Median latency: **0.452743 s**
- Min latency: **0.364816 s**
- Max latency: **0.527901 s**
- Stdev: **0.058968 s**
- Artifact: `reports/harness-refinement-2026-07-10-baseline.json`

### Quality baseline
- Validation gate: **PASS** (18/18)
- Observed validation runtime: **3.540765 s**
- Benchmark artifact summary fields: `avg_seconds`, `median_seconds`, `stdev_seconds`, `min_seconds`, `max_seconds`

## Candidate Hypothesis
Add a `p95_seconds` tail-latency field to the benchmark JSON payload and lock the percentile calculation with a targeted unit test. This should improve the nightly evidence trail with minimal risk and make future apply/reject decisions more sensitive to tail regressions.

## Successful Candidates
### Candidate A
- Change:
  - Added nearest-rank percentile support and emitted `p95_seconds` from `tests/benchmark_runner.py`
  - Added `test_nearest_rank_percentile_uses_tail_trial` to `tests/test_benchmark_runner.py`
  - Extended the latency summary field coverage test to assert `p95_seconds`
- Files touched:
  - `tests/benchmark_runner.py`
  - `tests/test_benchmark_runner.py`

### Candidate A Results
- Trials: 7/7 pass
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.354977 s**
- Median latency: **0.349732 s**
- Min latency: **0.304465 s**
- Max latency: **0.424290 s**
- P95 latency: **0.424290 s**
- Stdev: **0.033455 s**
- Artifact: `reports/harness-refinement-2026-07-10-candidate.json`
- Validation gate: **PASS** (19/19)
- Observed validation runtime: **1.244961 s**

## Failed Candidates
- None in this cycle.

## Comparison
### Quality delta
- Validation result: **PASS -> PASS**
- Validation coverage count: **18 -> 19** (**+5.56%**)
- Benchmark artifact summary fields: **5 -> 6**
- New evidence dimension added: `p95_seconds`
- Functional coverage added for percentile behavior and payload presence

### Reliability delta
- Pass rate: **100% -> 100%**
- Error rate: **0% -> 0%**
- Critical reliability regression: **none**

### Latency / throughput delta
- Avg latency: **0.440156 s -> 0.354977 s**
- Latency change: **-19.35%**
- Relative throughput change: **+24.00%**
- Stdev change: **0.058968 s -> 0.033455 s** (**-43.27%**)
- Validation runtime change: **3.540765 s -> 1.244961 s** (**-64.84%**)

## Acceptance Decision
**APPLY**

Reason: the candidate preserved 100% reliability, expanded the evidence trail with a reproducible tail-latency metric, and the observed benchmark/validation runs showed no regression. The new percentile behavior is explicitly covered by a unit test, making the gain measurable and repeatable.

## Final State
- Candidate left applied in the repository
- Small reversible commit created for the code change and today's report artifacts

## Files Touched
- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/harness-refinement-2026-07-10.md`
- `reports/harness-refinement-2026-07-10-baseline.json`
- `reports/harness-refinement-2026-07-10-candidate.json`

## Report Paths
- `reports/harness-refinement-2026-07-10.md`
- `reports/harness-refinement-2026-07-10-baseline.json`
- `reports/harness-refinement-2026-07-10-candidate.json`

## Generated Artifacts
- Benchmark JSON: `reports/harness-refinement-2026-07-10-baseline.json`
- Benchmark JSON: `reports/harness-refinement-2026-07-10-candidate.json`

## Failure Traces / Blockers
- No functional blockers encountered.
- Non-blocking note: Git warned that `tests/benchmark_runner.py` and `tests/test_benchmark_runner.py` will normalize `LF` to `CRLF` on a future Windows checkout/touch.

## Next Hypothesis
Add optional percentile expansion for both p50 and p95 in a compact summary block or JSONL history mode, so nightly runs can compare both central tendency and tail behavior across multiple benchmark executions without relying on raw trial arrays alone.
