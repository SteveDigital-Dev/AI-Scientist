# AI Scientist Harness Refinement Report - 2026-07-18

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Run type: nightly harness refinement
- Goal: run one measured refinement cycle and preserve the full evidence trail

## Fixed benchmark set
1. Passing smoke benchmark
   - Command: `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-18-harness-refinement/baseline-cli-smoke.json`
   - Candidate command: `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-18-harness-refinement/candidate-cli-smoke.json`
2. Fixed failing benchmark
   - Command: `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-18-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-18-harness-refinement/baseline-failure.json`
   - Candidate command: `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-18-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-18-harness-refinement/candidate-failure.json`
   - Direct trace capture: `python -m unittest discover -s reports/refinement/2026-07-18-harness-refinement/failure-fixture -p test_failure_fixture.py -v`
3. Validation gate
   - Command: `python -m unittest -v tests.test_benchmark_runner tests.test_cli_smoke_fixture tests.test_reuse_discovery_fixture`

## Baseline
### Passing smoke benchmark
- Successful trials: **5**
- Failed trials: **0**
- Pass rate: **1.00**
- Error rate: **0.00**
- Avg latency: **0.000572980 s**
- Median latency: **0.000453200 s**
- Throughput: **1745.261623 trials/s**
- Artifact: `reports/refinement/2026-07-18-harness-refinement/baseline-cli-smoke.json`

### Fixed failing benchmark
- Successful trials: **0**
- Failed trials: **3**
- Pass rate: **0.00**
- Error rate: **1.00**
- Avg latency: **0.002108600 s**
- Median latency: **0.001722500 s**
- Throughput: **474.248319 trials/s**
- Inline failure summaries in JSON: **0 / 3 failed trials**
- Artifact: `reports/refinement/2026-07-18-harness-refinement/baseline-failure.json`
- Trace artifact: `reports/refinement/2026-07-18-harness-refinement/baseline-failure-trace.txt`

## Candidate hypothesis
Add compact per-trial `failure_summaries` to benchmark JSON so failed runs preserve first-order failure evidence without requiring a separate repro command.

## Successful candidates
### Candidate A
- Change:
  - Added `_collect_failure_summaries(...)` and per-trial `failure_summaries` emission in `tests/benchmark_runner.py`
  - Added a regression test that verifies a failing run includes the failing test id and exception summary in `tests/test_benchmark_runner.py`
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
- Avg latency: **0.000337340 s**
- Median latency: **0.000318300 s**
- Throughput: **2964.368278 trials/s**
- Artifact: `reports/refinement/2026-07-18-harness-refinement/candidate-cli-smoke.json`

### Fixed failing benchmark
- Successful trials: **0**
- Failed trials: **3**
- Pass rate: **0.00**
- Error rate: **1.00**
- Avg latency: **0.001293600 s**
- Median latency: **0.001132700 s**
- Throughput: **773.036485 trials/s**
- Inline failure summaries in JSON: **3 / 3 failed trials**
- Failure summary example: `AssertionError: 'baseline' != 'candidate'`
- Artifact: `reports/refinement/2026-07-18-harness-refinement/candidate-failure.json`
- Trace artifact: `reports/refinement/2026-07-18-harness-refinement/candidate-failure-trace.txt`

### Validation gate
- Result: **PASS**
- Tests: **8 / 8**

## Baseline vs candidate
### Quality delta
- Inline failure summary coverage: **0 / 3 -> 3 / 3 failed trials**
- JSON failure evidence fields: **+1** (`trials[].failure_summaries`)
- Validation guard count: **7 -> 8** tests

### Reliability / error-rate delta
- Passing smoke benchmark: **5 / 5 pass -> 5 / 5 pass**, error rate **0.00 -> 0.00**
- Fixed failing benchmark: **0 / 3 pass -> 0 / 3 pass**, error rate **1.00 -> 1.00**
- Critical reliability regression: **none**

### Latency / throughput delta
- Passing smoke avg latency: **0.000572980 s -> 0.000337340 s** (**-41.12%**)
- Passing smoke throughput: **1745.261623 -> 2964.368278 trials/s** (**+69.85%**)
- Fixed failing benchmark avg latency: **0.002108600 s -> 0.001293600 s** (**-38.65%**)
- Fixed failing benchmark throughput: **474.248319 -> 773.036485 trials/s** (**+62.99%**)

## Acceptance decision
**APPLY**

Reason: the candidate produced a measurable quality gain by embedding actionable failure evidence directly in the benchmark payload, preserved reliability on both fixed benchmarks, and showed no latency or throughput regression in this run.

## Final state
- Candidate left applied in the repository
- Small reversible commit created for the code change and today’s evidence bundle

## Files touched
- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/refinement/2026-07-18-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-18-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-18-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-18-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-18-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-18-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-18-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-18-harness-refinement/report.md`

## Report paths
- `reports/refinement/2026-07-18-harness-refinement/report.md`
- `reports/refinement/2026-07-18-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-18-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-18-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-18-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-18-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-18-harness-refinement/candidate-failure-trace.txt`

## Generated artifacts
- `reports/refinement/2026-07-18-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-18-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-18-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-18-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-18-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-18-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-18-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-18-harness-refinement/report.md`

## Failure traces / blockers
- Baseline and candidate direct failure traces captured for the fixed failing benchmark
- No blockers encountered during the refinement cycle

## Next hypothesis
Add an optional top-level failure summary rollup (`failed_tests`, `first_failure`, `failure_count`) so downstream tooling can read the most important failure signal without scanning every trial entry.
