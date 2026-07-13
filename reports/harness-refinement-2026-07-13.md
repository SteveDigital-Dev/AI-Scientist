# AI Scientist Harness Refinement Report - 2026-07-13

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
- Avg latency: **0.343058 s**
- Median latency: **0.345626 s**
- Min latency: **0.283842 s**
- Max latency: **0.415356 s**
- P95 latency: **0.415356 s**
- Stdev: **0.042615 s**
- Derived throughput: **2.914960 trials/s**
- Artifact: `reports/harness-refinement-2026-07-13-baseline.json`

### Quality baseline
- Validation gate: **PASS** (19/19)
- Observed validation runtime: **2.602933 s**
- Benchmark artifact summary fields: `avg_seconds`, `median_seconds`, `stdev_seconds`, `min_seconds`, `max_seconds`, `p95_seconds`, `pass_rate`, `error_rate`

## Candidate Hypothesis
Add explicit `successful_trials`, `failed_trials`, and `throughput_trials_per_second` fields to the benchmark payload, and lock them with unit-test coverage. This should improve the nightly evidence trail for acceptance/rejection decisions without introducing meaningful reliability risk.

## Successful Candidates
### Candidate A
- Change:
  - Added `successful_trials`, `failed_trials`, and `throughput_trials_per_second` to `tests/benchmark_runner.py`
  - Extended `test_output_includes_latency_summary_fields` in `tests/test_benchmark_runner.py` to assert the new evidence fields
- Files touched:
  - `tests/benchmark_runner.py`
  - `tests/test_benchmark_runner.py`

## Candidate A Results
- Trials: 5/5 pass
- Successful trials: **5**
- Failed trials: **0**
- Pass rate: **100%**
- Error rate: **0%**
- Avg latency: **0.318783 s**
- Median latency: **0.326154 s**
- Min latency: **0.259242 s**
- Max latency: **0.368952 s**
- P95 latency: **0.368952 s**
- Stdev: **0.037031 s**
- Throughput: **3.136930 trials/s**
- Artifact: `reports/harness-refinement-2026-07-13-candidate.json`
- Validation gate: **PASS** (19/19)
- Observed validation runtime: **1.512982 s**

## Failed Candidates
- None in this cycle.

## Comparison
### Quality delta
- Validation result: **PASS -> PASS**
- Validation coverage count: **19 -> 19**
- Benchmark evidence fields added: **+3**
- New evidence dimensions added: `successful_trials`, `failed_trials`, `throughput_trials_per_second`
- Functional coverage added for explicit trial outcome counts and derived throughput presence

### Reliability delta
- Successful trials: **5 -> 5**
- Failed trials: **0 -> 0**
- Pass rate: **100% -> 100%**
- Error rate: **0% -> 0%**
- Critical reliability regression: **none**

### Latency / throughput delta
- Avg latency: **0.343058 s -> 0.318783 s**
- Latency change: **-7.08%**
- Throughput: **2.914960 -> 3.136930 trials/s**
- Throughput change: **+7.61%**
- Stdev change: **0.042615 s -> 0.037031 s** (**-13.10%**)
- Validation runtime change: **2.602933 s -> 1.512982 s** (**-41.87%**)

## Acceptance Decision
**APPLY**

Reason: the candidate preserved 100% reliability, expanded the benchmark payload with directly decision-useful evidence fields, and reproduced a modest benchmark speedup with no critical regression.

## Final State
- Candidate left applied in the repository
- Small reversible commit created for the code change and today's report artifacts

## Files Touched
- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/harness-refinement-2026-07-13.md`
- `reports/harness-refinement-2026-07-13-baseline.json`
- `reports/harness-refinement-2026-07-13-candidate.json`

## Report Paths
- `reports/harness-refinement-2026-07-13.md`
- `reports/harness-refinement-2026-07-13-baseline.json`
- `reports/harness-refinement-2026-07-13-candidate.json`

## Generated Artifacts
- Benchmark JSON: `reports/harness-refinement-2026-07-13-baseline.json`
- Benchmark JSON: `reports/harness-refinement-2026-07-13-candidate.json`

## Failure Traces / Blockers
- No functional blockers encountered.
- Non-blocking note: Git warned that `tests/benchmark_runner.py` and `tests/test_benchmark_runner.py` will normalize `LF` to `CRLF` on a future Windows checkout/touch.

## Next Hypothesis
Add an optional compact summary block that groups reliability, latency, and throughput fields for easier machine diffing across nightly reports without re-reading the raw trial array.
