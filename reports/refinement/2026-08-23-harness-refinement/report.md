# Nightly Harness Refinement Report

Date: 2026-08-23
Repo: `D:\GitHub\AI-Scientist`
Decision: Apply candidate and commit
Success signal: Fixed benchmark set remained reproducibly green while failing payloads now expose normalized per-test failure rates

## Hypothesis

Downstream consumers can already see which tests failed and how often they failed, but they still cannot distinguish a flaky test from a persistent failure without manually dividing counts by total trials. Adding deterministic `failed_test_rates` evidence should improve triage while preserving the current benchmark contract.

## Fixed benchmark set

Measured with `reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py`:

1. `cli_smoke`
2. `default_loader_isolation`
3. `repeated_temp_fixture`

## Baseline artifacts

- `reports/refinement/2026-08-23-harness-refinement/baseline.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/baseline-recheck.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-recheck-failure-trace.txt`

Baseline summary, fixed set, initial 5-trial sample:
- Successful trials: `5/5`
- Failed trials: `0/5`
- Pass rate: `1.0`
- Error rate: `0.0`
- Average latency: `0.076651600s`
- Median latency: `0.053238400s`
- Throughput: `13.046042 trials/s`

Baseline summary, fixed set, 10-trial reproducibility check:
- Successful trials: `10/10`
- Failed trials: `0/10`
- Pass rate: `1.0`
- Error rate: `0.0`
- Average latency: `0.192034220s`
- Median latency: `0.097338850s`
- Throughput: `5.207405 trials/s`

Baseline failing-payload summary:
- Failed trials: `3/3`
- Error rate: `1.0`
- `failed_test_counts`: `{"test_failure_fixture.FailureFixtureTest.test_expected_failure_signal": 3}`
- `failed_test_rates`: absent

## Candidate

Accepted candidate:
- `tests/benchmark_runner.py`
  - add top-level `failed_test_rates`
  - mirror `failed_test_rates` into `summary.failures`
- `tests/test_benchmark_runner.py`
  - add regression assertions for empty and repeated-failure `failed_test_rates`
- `reports/refinement/2026-08-23-harness-refinement/failure-fixture/test_failure_fixture.py`
  - fixed expected-failure fixture for controlled failure-path measurements

Failed candidates:
- None in this cycle

Candidate artifacts:
- `reports/refinement/2026-08-23-harness-refinement/candidate.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/candidate-recheck.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-recheck-failure-trace.txt`

Candidate summary, fixed set, initial 5-trial sample:
- Successful trials: `5/5`
- Failed trials: `0/5`
- Pass rate: `1.0`
- Error rate: `0.0`
- Average latency: `0.089149640s`
- Median latency: `0.071365700s`
- Throughput: `11.217095 trials/s`

Candidate summary, fixed set, 10-trial reproducibility check:
- Successful trials: `10/10`
- Failed trials: `0/10`
- Pass rate: `1.0`
- Error rate: `0.0`
- Average latency: `0.190916340s`
- Median latency: `0.111342050s`
- Throughput: `5.237896 trials/s`

Candidate failing-payload summary:
- Failed trials: `3/3`
- Error rate: `1.0`
- `failed_test_counts`: `{"test_failure_fixture.FailureFixtureTest.test_expected_failure_signal": 3}`
- `failed_test_rates`: `{"test_failure_fixture.FailureFixtureTest.test_expected_failure_signal": 1.0}`

## Deltas

Candidate vs baseline, fixed set, initial 5-trial sample:
- Quality delta: `+1` top-level evidence field (`failed_test_rates`)
- Quality delta: `+1` mirrored nested evidence field (`summary.failures.failed_test_rates`)
- Reliability delta: no change in pass rate (`1.0 -> 1.0`)
- Reliability delta: no change in error rate (`0.0 -> 0.0`)
- Latency delta: `+0.012498040s` average (`+16.31%`, slower)
- Median latency delta: `+0.018127300s` (`+34.05%`, slower)
- Throughput delta: `-1.828947 trials/s` (`-14.02%`)

Candidate vs baseline, fixed set, 10-trial reproducibility check:
- Quality delta: persistent-vs-flaky failure evidence is explicit instead of inferred
- Reliability delta: no change in pass rate (`1.0 -> 1.0`)
- Reliability delta: no change in error rate (`0.0 -> 0.0`)
- Latency delta: `-0.001117880s` average (`-0.58%`, faster)
- Median latency delta: `+0.014003200s` (`+14.39%`, slower)
- Throughput delta: `+0.030491 trials/s` (`+0.59%`)

Candidate vs baseline, failing payload:
- Reliability delta: no change in error rate (`1.0 -> 1.0`)
- Latency delta: `+0.000247733s` average (`+17.85%`, slower in absolute terms by ~0.25 ms`)
- Throughput delta: `-109.119353 trials/s` (`-15.15%`)

## Decision

Apply candidate.

Reason:
- The added `failed_test_rates` field is a measurable and reproducible quality gain on the failure path.
- The fixed benchmark set stayed green across both the initial `5/5` sample and the `10/10` reproducibility pass.
- The initial throughput regression did not reproduce against the frozen baseline artifact. The remaining failure-path slowdown is tiny in absolute terms and does not indicate a critical reliability regression.

## Validation

- `python -m unittest tests.test_benchmark_runner -v`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label baseline --module-path tests/benchmark_runner.py --output reports/refinement/2026-08-23-harness-refinement/baseline.json --failure-trace reports/refinement/2026-08-23-harness-refinement/baseline-failure-trace.txt --trials 5`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label candidate --module-path tests/benchmark_runner.py --output reports/refinement/2026-08-23-harness-refinement/candidate.json --failure-trace reports/refinement/2026-08-23-harness-refinement/candidate-failure-trace.txt --trials 5`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label baseline-recheck --module-path reports/refinement/2026-08-23-harness-refinement/artifacts/baseline/benchmark_runner.py --output reports/refinement/2026-08-23-harness-refinement/baseline-recheck.json --failure-trace reports/refinement/2026-08-23-harness-refinement/baseline-recheck-failure-trace.txt --trials 10`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label candidate-recheck --module-path tests/benchmark_runner.py --output reports/refinement/2026-08-23-harness-refinement/candidate-recheck.json --failure-trace reports/refinement/2026-08-23-harness-refinement/candidate-recheck-failure-trace.txt --trials 10`
- `python reports/refinement/2026-08-23-harness-refinement/artifacts/baseline/benchmark_runner.py --start-dir reports/refinement/2026-08-23-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-08-23-harness-refinement/baseline-failure.json`
- `python tests/benchmark_runner.py --start-dir reports/refinement/2026-08-23-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-08-23-harness-refinement/candidate-failure.json`
- `python -m unittest discover -s reports/refinement/2026-08-23-harness-refinement/failure-fixture -p test_failure_fixture.py -v`

## Touched files

- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/refinement/2026-08-23-harness-refinement/artifacts/baseline/benchmark_runner.py`
- `reports/refinement/2026-08-23-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-08-23-harness-refinement/baseline.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/baseline-recheck.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-recheck-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/candidate.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/candidate-recheck.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-recheck-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/report.md`

## Report paths

- `reports/refinement/2026-08-23-harness-refinement/report.md`
- `reports/refinement/2026-08-23-harness-refinement/baseline.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/baseline-recheck.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/candidate-recheck.json`

## Generated artifacts

- `reports/refinement/2026-08-23-harness-refinement/artifacts/baseline/benchmark_runner.py`
- `reports/refinement/2026-08-23-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-08-23-harness-refinement/baseline.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/baseline-recheck.json`
- `reports/refinement/2026-08-23-harness-refinement/baseline-recheck-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/candidate.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/candidate-recheck.json`
- `reports/refinement/2026-08-23-harness-refinement/candidate-recheck-failure-trace.txt`
- `reports/refinement/2026-08-23-harness-refinement/report.md`

## Failure traces and blockers

- `reports/refinement/2026-08-23-harness-refinement/baseline-failure-trace.txt` captures the expected failure fixture trace
- `reports/refinement/2026-08-23-harness-refinement/candidate-failure-trace.txt` captures the same expected failure fixture trace
- Blocker encountered: the first 5-trial timing sample suggested a slowdown, so a frozen-baseline reproducibility pass was added before making the accept/reject decision

## Next hypothesis

Add per-test first-seen and last-seen failing trial indices so downstream tooling can tell whether a failure clustered early, late, or throughout the run without replaying every trial payload.
