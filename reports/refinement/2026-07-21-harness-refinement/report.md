# AI Scientist Harness Refinement Report - 2026-07-21

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Run type: nightly harness refinement
- Goal: run one measured refinement cycle and preserve the full evidence trail

## Fixed benchmark set
1. Passing smoke benchmark
   - Baseline command: `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-21-harness-refinement/baseline-cli-smoke.json`
   - Candidate command: `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-21-harness-refinement/candidate-cli-smoke.json`
2. Fixed failing benchmark
   - Baseline command: `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-21-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-21-harness-refinement/baseline-failure.json`
   - Candidate command: `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-21-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-21-harness-refinement/candidate-failure.json`
   - Direct trace capture:
     - Baseline: `python -m unittest discover -s reports/refinement/2026-07-21-harness-refinement/failure-fixture -p test_failure_fixture.py -v`
     - Candidate: `python -m unittest discover -s reports/refinement/2026-07-21-harness-refinement/failure-fixture -p test_failure_fixture.py -v`
3. Validation gate
   - Command: `python -m unittest -v tests.test_benchmark_runner tests.test_cli_smoke_fixture tests.test_reuse_discovery_fixture`

## Baseline
### Passing smoke benchmark
- Successful trials: **5**
- Failed trials: **0**
- Pass rate: **1.00**
- Error rate: **0.00**
- Avg latency: **0.000551440008 s**
- Median latency: **0.000431000022 s**
- Throughput: **1813.433892 trials/s**
- Payload schema marker: **absent**
- Artifact: `reports/refinement/2026-07-21-harness-refinement/baseline-cli-smoke.json`

### Fixed failing benchmark
- Successful trials: **0**
- Failed trials: **3**
- Pass rate: **0.00**
- Error rate: **1.00**
- Avg latency: **0.003221833331 s**
- Median latency: **0.003325300000 s**
- Throughput: **310.382288 trials/s**
- Payload schema marker: **absent**
- Artifact: `reports/refinement/2026-07-21-harness-refinement/baseline-failure.json`
- Trace artifact: `reports/refinement/2026-07-21-harness-refinement/baseline-failure-trace.txt`

## Candidate hypothesis
Add a stable payload schema marker so downstream consumers can detect benchmark result format revisions without inferring them from field shape.

## Successful candidates
### Candidate A
- Change:
  - Added `SCHEMA_VERSION = "benchmark-runner.v2"` in `tests/benchmark_runner.py`
  - Emitted `schema_version` at the top level and mirrored it into `summary.metadata.schema_version`
  - Added regression assertions for the new schema marker in `tests/test_benchmark_runner.py`
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
- Avg latency: **0.000478860002 s**
- Median latency: **0.000428500003 s**
- Throughput: **2088.293018 trials/s**
- Payload schema marker: **`benchmark-runner.v2`**
- Artifact: `reports/refinement/2026-07-21-harness-refinement/candidate-cli-smoke.json`

### Fixed failing benchmark
- Successful trials: **0**
- Failed trials: **3**
- Pass rate: **0.00**
- Error rate: **1.00**
- Avg latency: **0.001910299994 s**
- Median latency: **0.001615799993 s**
- Throughput: **523.477989 trials/s**
- Payload schema marker: **`benchmark-runner.v2`**
- Artifact: `reports/refinement/2026-07-21-harness-refinement/candidate-failure.json`
- Trace artifact: `reports/refinement/2026-07-21-harness-refinement/candidate-failure-trace.txt`

### Validation gate
- Result: **PASS**
- Tests: **8 / 8**

## Baseline vs candidate
### Quality delta
- Stable payload contract marker: **+1** top-level field (`schema_version`)
- Mirrored summary metadata marker: **+1** nested field (`summary.metadata.schema_version`)
- Downstream payload-version detection: **improved** from implicit to explicit

### Reliability / error-rate delta
- Passing smoke benchmark: **5 / 5 pass -> 5 / 5 pass**, error rate **0.00 -> 0.00**
- Fixed failing benchmark: **0 / 3 pass -> 0 / 3 pass**, error rate **1.00 -> 1.00**
- Validation gate: **8 / 8 pass**
- Critical reliability regression: **none**

### Latency / throughput delta
- Passing smoke avg latency: **0.000551440008 s -> 0.000478860002 s** (**-13.16%**)
- Passing smoke throughput: **1813.433892 -> 2088.293018 trials/s** (**+15.16%**)
- Fixed failing benchmark avg latency: **0.003221833331 s -> 0.001910299994 s** (**-40.71%**)
- Fixed failing benchmark throughput: **310.382288 -> 523.477989 trials/s** (**+68.66%**)
- Note: the candidate targets payload clarity, not performance; the positive timing movement in this microbenchmark is welcome but secondary.

## Acceptance decision
**APPLY**

Reason: the candidate adds explicit, reproducible schema-version evidence to every benchmark payload, preserves reliability on the fixed benchmark set, passes the validation gate, and introduces no critical reliability regression.

## Final state
- Candidate left applied in the repository
- Small reversible commit created for the code change and today's evidence bundle

## Files touched
- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/refinement/2026-07-21-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-21-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-21-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-21-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-21-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-21-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-21-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-21-harness-refinement/report.md`

## Report paths
- `reports/refinement/2026-07-21-harness-refinement/report.md`
- `reports/refinement/2026-07-21-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-21-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-21-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-21-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-21-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-21-harness-refinement/candidate-failure-trace.txt`

## Generated artifacts
- `reports/refinement/2026-07-21-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-21-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-21-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-21-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-21-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-21-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-21-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-21-harness-refinement/report.md`

## Failure traces / blockers
- Baseline and candidate direct failure traces captured for the fixed failing benchmark
- Temporary blocker encountered during validation: a new assertion in `tests/test_benchmark_runner.py` initially sat outside the `TemporaryDirectory()` scope, causing a `FileNotFoundError`; fixed before final validation

## Next hypothesis
Add a stable run identifier or artifact digest field so downstream systems can distinguish payload schema version from per-artifact content identity.
