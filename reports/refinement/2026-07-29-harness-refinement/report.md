# Nightly Harness Refinement Report

Date: 2026-07-29
Repo: `D:\GitHub\AI-Scientist`
Decision: Apply candidate and commit
Success signal: Fixed benchmark set remained `5/5` passing and the candidate adds reproducible per-test failure frequency evidence to failing payloads

## Hypothesis

Downstream consumers can already see which tests failed, but they cannot tell how often a given test failed across repeated trials without scanning every trial entry. Adding a deterministic `failed_test_counts` rollup should improve failure triage while preserving the current reliability hardening.

## Fixed benchmark set

Measured with `reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py` over 5 trials:

1. `cli_smoke`
2. `default_loader_isolation`
3. `repeated_temp_fixture`

## Baseline artifacts

- `reports/refinement/2026-07-29-harness-refinement/baseline.json`
- `reports/refinement/2026-07-29-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-29-harness-refinement/baseline-failure-trace.txt`

Baseline summary:
- Successful trials: `5/5`
- Failed trials: `0/5`
- Pass rate: `1.0`
- Error rate: `0.0`
- Average latency: `0.081267960s`
- Median latency: `0.070151700s`
- Throughput: `12.304972 trials/s`

Baseline failing-payload summary:
- Failed trials: `3/3`
- Error rate: `1.0`
- `failed_test_counts`: absent

## Candidate

Accepted candidate:
- `tests/benchmark_runner.py`
  - add `failed_test_counts` to the top-level failure rollup
  - mirror `failed_test_counts` into `summary.failures`
- `tests/test_benchmark_runner.py`
  - add regression assertions for empty and failing `failed_test_counts` payloads

Failed candidates:
- None in this cycle

Candidate artifacts:
- `reports/refinement/2026-07-29-harness-refinement/candidate.json`
- `reports/refinement/2026-07-29-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-29-harness-refinement/candidate-failure-trace.txt`

Candidate summary:
- Successful trials: `5/5`
- Failed trials: `0/5`
- Pass rate: `1.0`
- Error rate: `0.0`
- Average latency: `0.077387920s`
- Median latency: `0.062378000s`
- Throughput: `12.921913 trials/s`

Candidate failing-payload summary:
- Failed trials: `3/3`
- Error rate: `1.0`
- `failed_test_counts`: `{"test_failure_fixture.FailureFixtureTest.test_expected_failure_signal": 3}`

## Deltas

Candidate vs baseline:
- Quality delta: `+1` top-level evidence field (`failed_test_counts`)
- Quality delta: `+1` mirrored nested evidence field (`summary.failures.failed_test_counts`)
- Quality delta: repeated-failure frequency is explicit instead of inferred from per-trial scanning
- Reliability delta: no change in fixed benchmark pass rate (`1.0 -> 1.0`)
- Reliability delta: no change in fixed benchmark error rate (`0.0 -> 0.0`)
- Reliability delta: no change in failing-payload benchmark error rate (`1.0 -> 1.0`)
- Latency delta: `-0.003880040s` average on the fixed benchmark set (`-4.77%`, faster)
- Median latency delta: `-0.007773700s` on the fixed benchmark set (`-11.08%`, faster)
- Throughput delta: `+0.616941 trials/s` on the fixed benchmark set (`+5.01%`)
- Failing-payload latency delta: `-0.000296500s` average (`-23.48%`, faster)
- Failing-payload throughput delta: `+243.102625 trials/s` (`+30.69%`)

## Decision

Apply candidate.

Reason:
- The candidate adds measurable, durable failure-evidence quality without changing observed reliability.
- The fixed benchmark set stayed reproducibly green across `5/5` trials and the validation gate stayed green.
- Timing moved in the positive direction, but the quality gain is the primary acceptance reason.

## Validation

- `python -m unittest tests.test_benchmark_runner -v`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label baseline --module-path tests/benchmark_runner.py --output reports/refinement/2026-07-29-harness-refinement/baseline.json --failure-trace reports/refinement/2026-07-29-harness-refinement/baseline-failure-trace.txt --trials 5`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label candidate --module-path tests/benchmark_runner.py --output reports/refinement/2026-07-29-harness-refinement/candidate.json --failure-trace reports/refinement/2026-07-29-harness-refinement/candidate-failure-trace.txt --trials 5`
- `python reports/refinement/2026-07-29-harness-refinement/artifacts/baseline/benchmark_runner.py --start-dir reports/refinement/2026-07-29-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-29-harness-refinement/baseline-failure.json`
- `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-29-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-29-harness-refinement/candidate-failure.json`
- `python -m unittest discover -s reports/refinement/2026-07-29-harness-refinement/failure-fixture -p test_failure_fixture.py -v`

## Touched files

- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/refinement/2026-07-29-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-29-harness-refinement/artifacts/baseline/benchmark_runner.py`
- `reports/refinement/2026-07-29-harness-refinement/baseline.json`
- `reports/refinement/2026-07-29-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-29-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-29-harness-refinement/candidate.json`
- `reports/refinement/2026-07-29-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-29-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-29-harness-refinement/report.md`

## Report paths

- `reports/refinement/2026-07-29-harness-refinement/report.md`
- `reports/refinement/2026-07-29-harness-refinement/baseline.json`
- `reports/refinement/2026-07-29-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-29-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-29-harness-refinement/candidate.json`
- `reports/refinement/2026-07-29-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-29-harness-refinement/candidate-failure-trace.txt`

## Generated artifacts

- `reports/refinement/2026-07-29-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-07-29-harness-refinement/artifacts/baseline/benchmark_runner.py`
- `reports/refinement/2026-07-29-harness-refinement/baseline.json`
- `reports/refinement/2026-07-29-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-07-29-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-29-harness-refinement/candidate.json`
- `reports/refinement/2026-07-29-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-07-29-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-07-29-harness-refinement/report.md`

## Failure traces and blockers

- `reports/refinement/2026-07-29-harness-refinement/baseline-failure-trace.txt` captures the expected fixture failure
- `reports/refinement/2026-07-29-harness-refinement/candidate-failure-trace.txt` captures the same expected fixture failure
- Blocker encountered: baseline artifact generation initially raced the directory creation step; reran sequentially and preserved the baseline evidence

## Next hypothesis

Add a compact repeated-failure ratio or per-test first/last-trial range so downstream tooling can distinguish persistent failures from one-off flakes without replaying the full trial list.
