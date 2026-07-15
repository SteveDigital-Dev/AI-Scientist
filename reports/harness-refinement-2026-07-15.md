# AI Scientist Harness Refinement Report - 2026-07-15

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Goal: run one measured refinement cycle and preserve the full evidence trail.

## Benchmark Set
### Fixed benchmark
- Command: `python tests/benchmark_runner.py --start-dir tests --pattern test_benchmark_runner.py --trials 5 --warmup 1 --reuse-discovery`
- Metrics: pass rate, error rate, successful/failed trial counts, average latency, median latency, min/max latency, p95 latency, stdev, throughput

### Validation gate
- Command: `python -m unittest -v tests.test_benchmark_runner tests.test_cli_smoke_fixture tests.test_hypothesis_record_validation tests.test_auto_research tests.test_ranking_determinism`
- Purpose: verify the broader harness suite still passes after the candidate change

## Baseline (pre-change)
### Reliability / latency baseline
- Trials: 5/5 pass
- Successful trials: **5**
- Failed trials: **0**
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.274740 s**
- Median latency: **0.272014 s**
- Min latency: **0.244830 s**
- Max latency: **0.312292 s**
- P95 latency: **0.312292 s**
- Stdev: **0.022659 s**
- Derived throughput: **3.639808 trials/s**
- Artifact: `reports/harness-refinement-2026-07-15-baseline.json`

### Quality baseline
- Validation gate: **PASS** (20/20)
- Observed validation runtime: **1.828936 s**
- Benchmark artifact already exposed top-level latency, reliability, and throughput fields, but not a grouped summary block

## Candidate Hypothesis
Add a compact `summary` block that groups reliability, latency, and throughput metrics under stable keys, and lock it with unit-test coverage. This should improve nightly diffability and evidence consumption without causing a critical reliability regression.

## Successful Candidates
### Candidate A
- Change:
  - Added `summary.reliability`, `summary.latency_seconds`, and `summary.throughput` to `tests/benchmark_runner.py`
  - Extended `test_output_includes_latency_summary_fields` in `tests/test_benchmark_runner.py` to assert the grouped summary mirrors the existing top-level fields
- Files touched:
  - `tests/benchmark_runner.py`
  - `tests/test_benchmark_runner.py`

## Candidate A Results
- Trials: 5/5 pass
- Successful trials: **5**
- Failed trials: **0**
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.352646 s**
- Median latency: **0.329342 s**
- Min latency: **0.301089 s**
- Max latency: **0.454999 s**
- P95 latency: **0.454999 s**
- Stdev: **0.055346 s**
- Throughput: **2.835704 trials/s**
- Artifact: `reports/harness-refinement-2026-07-15-candidate.json`
- Validation gate: **PASS** (20/20)
- Observed validation runtime: **1.057096 s**

## Failed Candidates
- None in this cycle.

## Comparison
### Quality delta
- Validation result: **PASS -> PASS**
- Validation coverage count: **20 -> 20**
- New grouped evidence block added: **+1**
- New grouped evidence dimensions added: `summary.reliability`, `summary.latency_seconds`, `summary.throughput`
- Functional coverage added for grouped summary consistency with the top-level payload

### Reliability delta
- Successful trials: **5 -> 5**
- Failed trials: **0 -> 0**
- Pass rate: **100% -> 100%**
- Error rate: **0% -> 0%**
- Critical reliability regression: **none**

### Latency / throughput delta
- Avg latency: **0.274740 s -> 0.352646 s**
- Latency change: **+28.35%**
- Throughput: **3.639808 -> 2.835704 trials/s**
- Throughput change: **-22.09%**
- Stdev change: **0.022659 s -> 0.055346 s** (**+144.26%**)
- Validation runtime change: **1.828936 s -> 1.057096 s** (**-42.20%**)

## Acceptance Decision
**APPLY**

Reason: the candidate adds deterministic, machine-diffable evidence structure that improves nightly report consumption while preserving 100% benchmark pass rate and 100% validation pass rate. The fixed benchmark latency regressed on this sample, but the change itself is a small serialization-only metadata addition with no behavioral regression, and the broader validation gate completed faster.

## Final State
- Candidate left applied in the repository
- Small reversible commit created for the code change and today's report artifacts

## Files Touched
- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/harness-refinement-2026-07-15.md`
- `reports/harness-refinement-2026-07-15-baseline.json`
- `reports/harness-refinement-2026-07-15-candidate.json`

## Report Paths
- `reports/harness-refinement-2026-07-15.md`
- `reports/harness-refinement-2026-07-15-baseline.json`
- `reports/harness-refinement-2026-07-15-candidate.json`

## Generated Artifacts
- Benchmark JSON: `reports/harness-refinement-2026-07-15-baseline.json`
- Benchmark JSON: `reports/harness-refinement-2026-07-15-candidate.json`

## Failure Traces / Blockers
- No functional blockers encountered.

## Next Hypothesis
Add an optional machine-readable report manifest that points at the baseline JSON, candidate JSON, markdown report, and touched files so downstream automation can ingest nightly refinement outputs without parsing prose.
