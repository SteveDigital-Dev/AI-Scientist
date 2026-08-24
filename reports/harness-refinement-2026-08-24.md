# AI Scientist Harness Refinement Report - 2026-08-24

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
- Avg latency: **0.387759980024 s**
- Median latency: **0.380008200067 s**
- Min latency: **0.373734800029 s**
- Max latency: **0.406628799974 s**
- P95 latency: **0.406628799974 s**
- Stdev: **0.014451362384 s**
- Throughput: **2.578914925513 trials/s**
- Artifact: `reports/harness-refinement-2026-08-24-baseline.json`

### Quality baseline
- Validation gate: **PASS** (24/24)
- Observed validation runtime: **0.515 s**
- Failure-span evidence fields: **absent**
- Payload schema version: **`benchmark-runner.v2`**

## Candidate Hypothesis
Add explicit per-test first/last failed trial indexes to the benchmark payload so downstream tooling can distinguish persistent repeated failures from intermittent ones without replaying the full trial list. Because this extends the payload contract, bump the schema marker to `benchmark-runner.v3`.

## Successful Candidates
### Candidate A
- Change:
  - Added `failed_test_first_trials` and `failed_test_last_trials` to `tests/benchmark_runner.py`
  - Mirrored the new fields into `summary.failures`
  - Bumped `SCHEMA_VERSION` from `benchmark-runner.v2` to `benchmark-runner.v3`
  - Extended `tests/test_benchmark_runner.py` to cover empty, single-failure, and repeated-failure span behavior
- Files touched:
  - `tests/benchmark_runner.py`
  - `tests/test_benchmark_runner.py`

## Candidate A Results
- Trials: 5/5 pass
- Successful trials: **5**
- Failed trials: **0**
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.387546040001 s**
- Median latency: **0.379117600038 s**
- Min latency: **0.373862800072 s**
- Max latency: **0.410888299928 s**
- P95 latency: **0.410888299928 s**
- Stdev: **0.014534416052 s**
- Throughput: **2.580338583763 trials/s**
- Artifact: `reports/harness-refinement-2026-08-24-candidate.json`
- Validation gate: **PASS** (24/24)
- Observed validation runtime: **0.537 s**
- Failure-span evidence fields: **present**
- Payload schema version: **`benchmark-runner.v3`**

## Failed Candidates
- None in this cycle.

## Comparison
### Quality delta
- Validation result: **PASS -> PASS**
- Validation coverage count: **24 -> 24**
- New top-level evidence fields: **+2**
- New nested evidence fields: **+2** under `summary.failures`
- New evidence dimensions added: `failed_test_first_trials`, `failed_test_last_trials`
- Payload contract marker updated: **`benchmark-runner.v2` -> `benchmark-runner.v3`**
- Repeated-failure persistence is now explicit instead of inferred from per-trial scanning

### Reliability delta
- Successful trials: **5 -> 5**
- Failed trials: **0 -> 0**
- Pass rate: **100% -> 100%**
- Error rate: **0% -> 0%**
- Critical reliability regression: **none**

### Latency / throughput delta
- Avg latency: **0.387759980024 s -> 0.387546040001 s** (**-0.06%**)
- Median latency: **0.380008200067 s -> 0.379117600038 s** (**-0.23%**)
- Throughput: **2.578914925513 -> 2.580338583763 trials/s** (**+0.06%**)
- Stdev change: **0.014451362384 s -> 0.014534416052 s** (**+0.57%**)
- Validation runtime change: **0.515 s -> 0.537 s** (**+4.27%**)

## Acceptance Decision
**APPLY**

Reason: the candidate adds measurable, reproducible failure-persistence evidence, preserves 100% benchmark reliability and 100% validation pass rate, and does not introduce a critical reliability regression. Runtime movement is effectively neutral on the fixed benchmark set.

## Final State
- Candidate left applied in the repository
- Small reversible commit created for the code change and today's report artifacts

## Files Touched
- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/harness-refinement-2026-08-24.md`
- `reports/harness-refinement-2026-08-24-baseline.json`
- `reports/harness-refinement-2026-08-24-candidate.json`

## Report Paths
- `reports/harness-refinement-2026-08-24.md`
- `reports/harness-refinement-2026-08-24-baseline.json`
- `reports/harness-refinement-2026-08-24-candidate.json`

## Generated Artifacts
- Benchmark JSON: `reports/harness-refinement-2026-08-24-baseline.json`
- Benchmark JSON: `reports/harness-refinement-2026-08-24-candidate.json`
- Markdown report: `reports/harness-refinement-2026-08-24.md`

## Failure Traces / Blockers
- No benchmark or validation failure traces were produced in this cycle.
- No functional blockers encountered.

## Next Hypothesis
Add an explicit per-test trial-list field or compact persistence classification so downstream tooling can distinguish continuous failures from sparse recurring flakes without reconstructing the pattern from first/last indexes plus counts.
