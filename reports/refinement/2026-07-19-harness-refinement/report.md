# AI Scientist Harness Refinement Report - 2026-07-19

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Run type: nightly harness refinement
- Goal: run one measured refinement cycle and preserve the full evidence trail

## Fixed benchmark set
1. Passing smoke benchmark
   - Baseline command: `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-19-harness-refinement/baseline-cli-smoke.json`
   - Candidate command: `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-19-harness-refinement/candidate-cli-smoke.json`
2. Fixed failing benchmark
   - Baseline command: `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-19-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-19-harness-refinement/baseline-failure.json`
   - Candidate command: `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-19-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-19-harness-refinement/candidate-failure.json`
   - Direct trace capture:
     - Baseline: `python -m unittest discover -s reports/refinement/2026-07-19-harness-refinement/failure-fixture -p test_failure_fixture.py -v`
     - Candidate: `python -m unittest discover -s reports/refinement/2026-07-19-harness-refinement/failure-fixture -p test_failure_fixture.py -v`
3. Validation gate
   - Command: `python -m unittest -v tests.test_benchmark_runner tests.test_cli_smoke_fixture tests.test_reuse_discovery_fixture`

## Baseline
### Passing smoke benchmark
- Successful trials: **5**
- Failed trials: **0**
- Pass rate: **1.00**
- Error rate: **0.00**
- Avg latency: **0.000174920 s**
- Median latency: **0.000093800 s**
- Throughput: **5716.899188 trials/s**
- Artifact: `reports/refinement/2026-07-19-harness-refinement/baseline-cli-smoke.json`

### Fixed failing benchmark
- Successful trials: **0**
- Failed trials: **3**
- Pass rate: **0.00**
- Error rate: **1.00**
- Avg latency: **0.000866733 s**
- Median latency: **0.000448300 s**
- Throughput: **1153.757412 trials/s**
- Top-level failed test rollup fields: **absent**
- Artifact: `reports/refinement/2026-07-19-harness-refinement/baseline-failure.json`
- Trace artifact: `reports/refinement/2026-07-19-harness-refinement/baseline-failure-trace.txt`

## Candidate hypothesis
Add top-level failure rollup fields (`failed_tests`, `first_failure`, `failure_count`) so downstream tooling can read the most important failure signal without scanning every trial entry.

## Successful candidates
### Candidate A
- Change:
  - Added `_build_failure_rollup(...)` in `tests/benchmark_runner.py`
  - Emitted top-level failure rollup fields and mirrored them into `summary.failures`
  - Added regression assertions for passing and failing outputs in `tests/test_benchmark_runner.py`
- Files:
  - `tests/benchmark_runner.py`
  - `tests/test_benchmark_runner.py`

## Failed candidates
- None in this cycle.

## Candidate results
### Passing smoke benchmark
- Successful trials: **5**
- Failed trials: **0**
- Pass rate: **1.00**
- Error rate: **0.00**
- Avg latency: **0.000200040 s**
- Median latency: **0.000200000 s**
- Throughput: **4999.000100 trials/s**
- Top-level failed test rollup fields: `[]`, `null`, `0`
- Artifact: `reports/refinement/2026-07-19-harness-refinement/candidate-cli-smoke.json`

### Fixed failing benchmark
- Successful trials: **0**
- Failed trials: **3**
- Pass rate: **0.00**
- Error rate: **1.00**
- Avg latency: **0.000556100 s**
- Median latency: **0.000452600 s**
- Throughput: **1798.237743 trials/s**
- Top-level failed test rollup fields:
  - `failed_tests`: `["test_failure_fixture.FailureFixtureTest.test_expected_failure_signal"]`
  - `first_failure`: `{"test": "test_failure_fixture.FailureFixtureTest.test_expected_failure_signal", "message": "AssertionError: 'baseline' != 'candidate'"}`
  - `failure_count`: `3`
- Artifact: `reports/refinement/2026-07-19-harness-refinement/candidate-failure.json`
- Trace artifact: `reports/refinement/2026-07-19-harness-refinement/candidate-failure-trace.txt`

### Validation gate
- Result: **PASS**
- Tests: **8 / 8**

## Baseline vs candidate
### Quality delta
- Top-level failure evidence fields: **+3** (`failed_tests`, `first_failure`, `failure_count`)
- Summary failure rollup block: **+1** (`summary.failures`)
- Failed benchmark first-order failure readability: **improved**

### Reliability / error-rate delta
- Passing smoke benchmark: **5 / 5 pass -> 5 / 5 pass**, error rate **0.00 -> 0.00**
- Fixed failing benchmark: **0 / 3 pass -> 0 / 3 pass**, error rate **1.00 -> 1.00**
- Validation gate: **8 / 8 pass -> 8 / 8 pass**
- Critical reliability regression: **none**

### Latency / throughput delta
- Passing smoke avg latency: **0.000174920 s -> 0.000200040 s** (**+14.36% slower**)
- Passing smoke throughput: **5716.899188 -> 4999.000100 trials/s** (**-12.56%**)
- Fixed failing benchmark avg latency: **0.000866733 s -> 0.000556100 s** (**-35.84% faster**)
- Fixed failing benchmark throughput: **1153.757412 -> 1798.237743 trials/s** (**+55.86%**)
- Note: smoke-case movement is small absolute-time noise in a microbenchmark; the candidate's intended gain is the new failure rollup evidence.

## Acceptance decision
**APPLY**

Reason: the candidate added measurable, reproducible quality signal to failed benchmark payloads, preserved reliability on the fixed benchmark set and validation gate, and introduced no critical reliability regression.

## Final state
- Candidate left applied in the repository
- Small reversible commit created for the code change and today's evidence bundle

## Files touched
- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/refinement/2026-07-19-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-19-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-19-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-19-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-19-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-19-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-19-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-19-harness-refinement/report.md`

## Report paths
- `reports/refinement/2026-07-19-harness-refinement/report.md`
- `reports/refinement/2026-07-19-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-19-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-19-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-19-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-19-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-19-harness-refinement/candidate-failure-trace.txt`

## Generated artifacts
- `reports/refinement/2026-07-19-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-19-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-19-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-19-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-19-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-19-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-19-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-19-harness-refinement/report.md`

## Failure traces / blockers
- Baseline and candidate direct failure traces captured for the fixed failing benchmark
- No blockers encountered during the refinement cycle

## Next hypothesis
Add an optional per-run artifact hash or schema version field so downstream consumers can detect payload-shape changes and cache/report against stable benchmark result formats.
