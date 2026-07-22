# AI Scientist Harness Refinement Report - 2026-07-22

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Run type: nightly harness refinement
- Goal: run one measured refinement cycle and preserve the full evidence trail

## Fixed benchmark set
1. Passing smoke benchmark
   - Baseline command: `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-22-harness-refinement/baseline-cli-smoke.json`
   - Candidate command: `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-22-harness-refinement/candidate-cli-smoke.json`
2. Fixed failing benchmark
   - Baseline command: `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-22-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-22-harness-refinement/baseline-failure.json`
   - Candidate command: `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-22-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-22-harness-refinement/candidate-failure.json`
   - Direct trace capture:
     - Baseline: `python -m unittest discover -s reports/refinement/2026-07-22-harness-refinement/failure-fixture -p test_failure_fixture.py -v`
     - Candidate: `python -m unittest discover -s reports/refinement/2026-07-22-harness-refinement/failure-fixture -p test_failure_fixture.py -v`
3. Validation gate
   - Command: `python -m unittest -v tests.test_benchmark_runner tests.test_cli_smoke_fixture tests.test_reuse_discovery_fixture`

## Baseline
### Passing smoke benchmark
- Successful trials: **5**
- Failed trials: **0**
- Pass rate: **1.00**
- Error rate: **0.00**
- Avg latency: **0.000464440003 s**
- Median latency: **0.000434499991 s**
- Throughput: **2153.130637 trials/s**
- Benchmark config digest: **absent**
- Artifact: `reports/refinement/2026-07-22-harness-refinement/baseline-cli-smoke.json`

### Fixed failing benchmark
- Successful trials: **0**
- Failed trials: **3**
- Pass rate: **0.00**
- Error rate: **1.00**
- Avg latency: **0.001778699991 s**
- Median latency: **0.001647799974 s**
- Throughput: **562.208357 trials/s**
- Benchmark config digest: **absent**
- Artifact: `reports/refinement/2026-07-22-harness-refinement/baseline-failure.json`
- Trace artifact: `reports/refinement/2026-07-22-harness-refinement/baseline-failure-trace.txt`

## Candidate hypothesis
Add a deterministic benchmark-config digest so downstream consumers can identify the benchmark definition directly from the payload without parsing the command string or conflating configuration identity with schema version.

## Successful candidates
### Candidate A
- Change:
  - Added `_build_benchmark_config_digest(...)` in `tests/benchmark_runner.py`
  - Emitted `benchmark_config_digest` at the top level and mirrored it into `summary.metadata.benchmark_config_digest`
  - Added regression assertions for the new digest field in `tests/test_benchmark_runner.py`
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
- Avg latency: **0.000549959997 s**
- Median latency: **0.000545799994 s**
- Throughput: **1818.314070 trials/s**
- Benchmark config digest: **`74e8c13b86c94a44809e0abc1247bf7f19c7b3fca2b66139e74f990afa974e3b`**
- Artifact: `reports/refinement/2026-07-22-harness-refinement/candidate-cli-smoke.json`

### Fixed failing benchmark
- Successful trials: **0**
- Failed trials: **3**
- Pass rate: **0.00**
- Error rate: **1.00**
- Avg latency: **0.002177099998 s**
- Median latency: **0.001864500024 s**
- Throughput: **459.326628 trials/s**
- Benchmark config digest: **`7d8ed7e5321dd1515ced982818b02f5b0da55ccbe1428b3af9cc027e778975e9`**
- Artifact: `reports/refinement/2026-07-22-harness-refinement/candidate-failure.json`
- Trace artifact: `reports/refinement/2026-07-22-harness-refinement/candidate-failure-trace.txt`

### Validation gate
- Result: **PASS**
- Tests: **8 / 8**

## Baseline vs candidate
### Quality delta
- Stable benchmark identity field: **+1** top-level field (`benchmark_config_digest`)
- Mirrored summary metadata identity field: **+1** nested field (`summary.metadata.benchmark_config_digest`)
- Downstream benchmark-definition detection: **improved** from implicit command parsing to explicit deterministic digest

### Reliability / error-rate delta
- Passing smoke benchmark: **5 / 5 pass -> 5 / 5 pass**, error rate **0.00 -> 0.00**
- Fixed failing benchmark: **0 / 3 pass -> 0 / 3 pass**, error rate **1.00 -> 1.00**
- Validation gate: **8 / 8 pass**
- Critical reliability regression: **none**

### Latency / throughput delta
- Passing smoke avg latency: **0.000464440003 s -> 0.000549959997 s** (**+18.41%**)
- Passing smoke throughput: **2153.130637 -> 1818.314070 trials/s** (**-15.55%**)
- Fixed failing benchmark avg latency: **0.001778699991 s -> 0.002177099998 s** (**+22.40%**)
- Fixed failing benchmark throughput: **562.208357 -> 459.326628 trials/s** (**-18.30%**)
- Note: this candidate targets artifact identity, not runtime speed; the measured slowdown is small in absolute terms but real and should be tracked.

## Acceptance decision
**APPLY**

Reason: the candidate adds a reproducible benchmark-identity signal to every payload, preserves all observed reliability characteristics on the fixed benchmark set, passes the validation gate, and introduces no critical reliability regression. The latency/throughput regressions are measurable and documented, but they are small in absolute terms for this harness and do not outweigh the quality gain for downstream artifact handling.

## Final state
- Candidate left applied in the repository
- Small reversible commit created for the code change and today's evidence bundle

## Files touched
- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/refinement/2026-07-22-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-22-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-22-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-22-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-22-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-22-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-22-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-22-harness-refinement/report.md`

## Report paths
- `reports/refinement/2026-07-22-harness-refinement/report.md`
- `reports/refinement/2026-07-22-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-22-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-22-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-22-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-22-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-22-harness-refinement/candidate-failure-trace.txt`

## Generated artifacts
- `reports/refinement/2026-07-22-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-22-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-22-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-22-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-22-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-22-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-22-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-22-harness-refinement/report.md`

## Failure traces / blockers
- Baseline and candidate direct failure traces captured for the fixed failing benchmark
- No blocking failures encountered in this cycle

## Next hypothesis
Separate benchmark-definition identity from artifact-content identity by adding a second deterministic digest for the emitted payload content after normalizing volatile timing fields.
