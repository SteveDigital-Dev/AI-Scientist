# AI Scientist Harness Refinement Report - 2026-07-28

## Scope
- Repo: `D:\GitHub\AI-Scientist`
- Run type: nightly harness refinement
- Goal: run one measured refinement cycle and preserve the full evidence trail
- Base commit: `f30f0b9`

## Fixed benchmark set
1. Passing smoke benchmark
   - Baseline command: `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-28-harness-refinement/baseline-cli-smoke.json`
   - Candidate command: `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-28-harness-refinement/candidate-cli-smoke.json`
2. Fixed failing benchmark
   - Baseline command: `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-28-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-28-harness-refinement/baseline-failure.json`
   - Candidate command: `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-28-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-28-harness-refinement/candidate-failure.json`
   - Direct trace capture:
     - Baseline: `python -m unittest discover -s reports/refinement/2026-07-28-harness-refinement/failure-fixture -p test_failure_fixture.py -v`
     - Candidate: `python -m unittest discover -s reports/refinement/2026-07-28-harness-refinement/failure-fixture -p test_failure_fixture.py -v`
3. Validation gate
   - Command: `python -m unittest -v tests.test_benchmark_runner tests.test_cli_smoke_fixture tests.test_reuse_discovery_fixture`

## Baseline
### Passing smoke benchmark
- Successful trials: **5**
- Failed trials: **0**
- Pass rate: **1.00**
- Error rate: **0.00**
- Avg latency: **0.000132300030 s**
- Median latency: **0.000124900020 s**
- Throughput: **7558.577301 trials/s**
- Result digest field: **absent**
- Artifact: `reports/refinement/2026-07-28-harness-refinement/baseline-cli-smoke.json`

### Fixed failing benchmark
- Successful trials: **0**
- Failed trials: **3**
- Pass rate: **0.00**
- Error rate: **1.00**
- Avg latency: **0.000708866709 s**
- Median latency: **0.000591300079 s**
- Throughput: **1410.702445 trials/s**
- Result digest field: **absent**
- Artifact: `reports/refinement/2026-07-28-harness-refinement/baseline-failure.json`
- Trace artifact: `reports/refinement/2026-07-28-harness-refinement/baseline-failure-trace.txt`

## Candidate hypothesis
Add a stable per-artifact payload digest so downstream consumers can distinguish schema version from the identity of a specific benchmark result.

## Successful candidates
### Candidate A
- Change:
  - Added `_build_result_digest(...)` in `tests/benchmark_runner.py`
  - Emitted top-level `result_digest` for every benchmark payload
  - Mirrored the digest into `summary.metadata.result_digest`
  - Added regression assertions for both passing and failing payloads in `tests/test_benchmark_runner.py`
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
- Avg latency: **0.000169020006 s**
- Median latency: **0.000160700059 s**
- Throughput: **5916.459365 trials/s**
- Result digest field: **present**
- Artifact: `reports/refinement/2026-07-28-harness-refinement/candidate-cli-smoke.json`

### Fixed failing benchmark
- Successful trials: **0**
- Failed trials: **3**
- Pass rate: **0.00**
- Error rate: **1.00**
- Avg latency: **0.001121533336 s**
- Median latency: **0.001120600034 s**
- Throughput: **891.636448 trials/s**
- Result digest field: **present**
- Artifact: `reports/refinement/2026-07-28-harness-refinement/candidate-failure.json`
- Trace artifact: `reports/refinement/2026-07-28-harness-refinement/candidate-failure-trace.txt`

### Validation gate
- Result: **PASS**
- Tests: **10 / 10**

## Baseline vs candidate
### Quality delta
- Stable per-artifact identity marker: **+1** top-level field (`result_digest`)
- Mirrored summary metadata digest: **+1** nested field (`summary.metadata.result_digest`)
- Downstream artifact identity detection: **improved** from implicit to explicit

### Reliability / error-rate delta
- Passing smoke benchmark: **5 / 5 pass -> 5 / 5 pass**, error rate **0.00 -> 0.00**
- Fixed failing benchmark: **0 / 3 pass -> 0 / 3 pass**, error rate **1.00 -> 1.00**
- Validation gate: **10 / 10 pass**
- Critical reliability regression: **none**

### Latency / throughput delta
- Passing smoke avg latency: **0.000132300030 s -> 0.000169020006 s** (**+27.76%**, +0.000036719977 s)
- Passing smoke throughput: **7558.577301 -> 5916.459365 trials/s** (**-21.73%**)
- Fixed failing benchmark avg latency: **0.000708866709 s -> 0.001121533336 s** (**+58.21%**, +0.000412666627 s)
- Fixed failing benchmark throughput: **1410.702445 -> 891.636448 trials/s** (**-36.79%**)
- Note: this benchmark is extremely small, so percentage movement exaggerates an absolute cost that remains below half a millisecond per run.

## Acceptance decision
**APPLY**

Reason: the candidate adds deterministic, reproducible artifact-identity evidence to every payload, is covered by the validation gate, preserves the fixed benchmark pass/fail profile, and introduces no critical reliability regression. The latency penalty is measurable but remains very small in absolute terms for this harness.

## Final state
- Candidate left applied in the repository
- Small reversible commit to be created for the code change and today's evidence bundle

## Files touched
- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/refinement/2026-07-28-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-28-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-28-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-28-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-28-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-28-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-28-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-28-harness-refinement/report.md`

## Report paths
- `reports/refinement/2026-07-28-harness-refinement/report.md`
- `reports/refinement/2026-07-28-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-28-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-28-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-28-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-28-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-28-harness-refinement/candidate-failure-trace.txt`

## Generated artifacts
- `reports/refinement/2026-07-28-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-28-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-28-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-28-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-28-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-28-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-28-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-28-harness-refinement/report.md`

## Failure traces / blockers
- Baseline and candidate direct failure traces captured for the fixed failing benchmark
- No blocking validation failures encountered during the refinement cycle

## Next hypothesis
Add an optional digest scope marker so downstream consumers can tell whether `result_digest` covers the whole payload, a canonical summary subset, or another stable representation.
