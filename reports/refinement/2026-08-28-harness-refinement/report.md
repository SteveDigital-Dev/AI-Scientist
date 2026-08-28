# Nightly Harness Refinement Report

Date: 2026-08-28
Repo: `D:\GitHub\AI-Scientist`
Decision: Apply candidate and commit
Success signal: Fixed benchmark set stayed reproducibly green while failing payloads now include a representative per-test failure message rollup

## Hypothesis

Downstream triage can already tell which tests failed, how often they failed, and when they first and last failed, but it still cannot see a stable example failure message per test without replaying raw trial payloads. Adding a `failed_test_example_messages` rollup should improve failure-path evidence while preserving current reliability.

## Fixed benchmark set

Measured with `reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py`:

1. `cli_smoke`
2. `default_loader_isolation`
3. `repeated_temp_fixture`

## Baseline artifacts

- `reports/refinement/2026-08-28-harness-refinement/baseline.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/baseline-recheck.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-recheck-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/artifacts/baseline/benchmark_runner.py`

Baseline summary, fixed set, initial 5-trial sample:
- Successful trials: `5/5`
- Failed trials: `0/5`
- Pass rate: `1.0`
- Error rate: `0.0`
- Average latency: `0.084512940s`
- Median latency: `0.063966200s`
- Throughput: `11.832508 trials/s`

Baseline summary, fixed set, 10-trial reproducibility check:
- Successful trials: `10/10`
- Failed trials: `0/10`
- Pass rate: `1.0`
- Error rate: `0.0`
- Average latency: `0.062693870s`
- Median latency: `0.055191700s`
- Throughput: `15.950523 trials/s`

Baseline failing-payload summary:
- Failed trials: `3/3`
- Error rate: `1.0`
- `failed_test_counts`: `{"test_failure_fixture.FailureFixtureTest.test_expected_failure_signal": 3}`
- `failed_test_rates`: `{"test_failure_fixture.FailureFixtureTest.test_expected_failure_signal": 1.0}`
- `failed_test_example_messages`: absent

## Candidate

Accepted candidate:
- `tests/benchmark_runner.py`
  - add top-level `failed_test_example_messages`
  - mirror `failed_test_example_messages` into `summary.failures`
- `tests/test_benchmark_runner.py`
  - add regression assertions for empty, single-failure, and repeated-failure `failed_test_example_messages`

Failed candidates:
- None in this cycle

Candidate artifacts:
- `reports/refinement/2026-08-28-harness-refinement/candidate.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/candidate-recheck.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-recheck-failure-trace.txt`

Candidate summary, fixed set, initial 5-trial sample:
- Successful trials: `5/5`
- Failed trials: `0/5`
- Pass rate: `1.0`
- Error rate: `0.0`
- Average latency: `0.062293040s`
- Median latency: `0.050703900s`
- Throughput: `16.053158 trials/s`

Candidate summary, fixed set, 10-trial reproducibility check:
- Successful trials: `10/10`
- Failed trials: `0/10`
- Pass rate: `1.0`
- Error rate: `0.0`
- Average latency: `0.064238250s`
- Median latency: `0.057520900s`
- Throughput: `15.567049 trials/s`

Candidate failing-payload summary:
- Failed trials: `3/3`
- Error rate: `1.0`
- `failed_test_counts`: `{"test_failure_fixture.FailureFixtureTest.test_expected_failure_signal": 3}`
- `failed_test_rates`: `{"test_failure_fixture.FailureFixtureTest.test_expected_failure_signal": 1.0}`
- `failed_test_example_messages`: `{"test_failure_fixture.FailureFixtureTest.test_expected_failure_signal": "AssertionError: 'baseline' != 'candidate'"}`

## Deltas

Candidate vs baseline, fixed set, initial 5-trial sample:
- Quality delta: `+1` top-level evidence field (`failed_test_example_messages`)
- Quality delta: `+1` mirrored nested evidence field (`summary.failures.failed_test_example_messages`)
- Reliability delta: no change in pass rate (`1.0 -> 1.0`)
- Reliability delta: no change in error rate (`0.0 -> 0.0`)
- Latency delta: `-0.022219900s` average (`-26.29%`, faster)
- Median latency delta: `-0.013262300s` (`-20.73%`, faster)
- Throughput delta: `+4.220650 trials/s` (`+35.67%`)

Candidate vs baseline, fixed set, 10-trial reproducibility check:
- Quality delta: failing tests now retain one stable example failure message per test without replaying raw trial payloads
- Reliability delta: no change in pass rate (`1.0 -> 1.0`)
- Reliability delta: no change in error rate (`0.0 -> 0.0`)
- Latency delta: `+0.001544380s` average (`+2.46%`, slower)
- Median latency delta: `+0.002329200s` (`+4.22%`, slower)
- Throughput delta: `-0.383474 trials/s` (`-2.40%`)

Candidate vs baseline, failing payload:
- Quality delta: failing payload now includes `failed_test_example_messages`
- Reliability delta: no change in error rate (`1.0 -> 1.0`)
- Latency delta: `-0.000396533s` average (`-25.26%`, faster)
- Median latency delta: `-0.000471400s` (`-34.79%`, faster)
- Throughput delta: `+215.201167 trials/s` (`+33.79%`)

## Decision

Apply candidate.

Reason:
- The new failure-message rollup is a measurable quality gain on the failure path and does not require consumers to replay raw trial details for a representative message.
- The fixed benchmark set stayed green across both the initial `5/5` sample and the `10/10` reproducibility pass.
- The only reproduced performance movement on the green set was a small `+2.46%` average-latency increase with unchanged reliability, which is not a critical regression for a quality-only evidence improvement.
- The controlled failing payload preserved the same `3/3` failure detection while improving evidence richness and running faster in this sample.

## Validation

- `python -m unittest tests.test_benchmark_runner -v`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label baseline --module-path tests/benchmark_runner.py --output reports/refinement/2026-08-28-harness-refinement/baseline.json --failure-trace reports/refinement/2026-08-28-harness-refinement/baseline-failure-trace.txt --trials 5`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label candidate --module-path tests/benchmark_runner.py --output reports/refinement/2026-08-28-harness-refinement/candidate.json --failure-trace reports/refinement/2026-08-28-harness-refinement/candidate-failure-trace.txt --trials 5`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label baseline-recheck --module-path reports/refinement/2026-08-28-harness-refinement/artifacts/baseline/benchmark_runner.py --output reports/refinement/2026-08-28-harness-refinement/baseline-recheck.json --failure-trace reports/refinement/2026-08-28-harness-refinement/baseline-recheck-failure-trace.txt --trials 10`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label candidate-recheck --module-path tests/benchmark_runner.py --output reports/refinement/2026-08-28-harness-refinement/candidate-recheck.json --failure-trace reports/refinement/2026-08-28-harness-refinement/candidate-recheck-failure-trace.txt --trials 10`
- `python reports/refinement/2026-08-28-harness-refinement/artifacts/baseline/benchmark_runner.py --start-dir reports/refinement/2026-08-28-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-08-28-harness-refinement/baseline-failure.json`
- `python tests/benchmark_runner.py --start-dir reports/refinement/2026-08-28-harness-refinement/failure-fixture --pattern test_failure_fixture.py --trials 3 --warmup 0 --reuse-discovery --output reports/refinement/2026-08-28-harness-refinement/candidate-failure.json`
- `python -m unittest discover -s reports/refinement/2026-08-28-harness-refinement/failure-fixture -p test_failure_fixture.py -v`

## Touched files

- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/refinement/2026-08-28-harness-refinement/artifacts/baseline/benchmark_runner.py`
- `reports/refinement/2026-08-28-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-08-28-harness-refinement/baseline.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/baseline-recheck.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-recheck-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/candidate.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/candidate-recheck.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-recheck-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/failure-fixture-discover-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/report.md`

## Report paths

- `reports/refinement/2026-08-28-harness-refinement/report.md`
- `reports/refinement/2026-08-28-harness-refinement/baseline.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/baseline-recheck.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/candidate-recheck.json`
- `reports/refinement/2026-08-28-harness-refinement/failure-fixture-discover-trace.txt`

## Generated artifacts

- `reports/refinement/2026-08-28-harness-refinement/artifacts/baseline/benchmark_runner.py`
- `reports/refinement/2026-08-28-harness-refinement/failure-fixture/test_failure_fixture.py`
- `reports/refinement/2026-08-28-harness-refinement/baseline.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-failure.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/baseline-recheck.json`
- `reports/refinement/2026-08-28-harness-refinement/baseline-recheck-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/candidate.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-failure.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/candidate-recheck.json`
- `reports/refinement/2026-08-28-harness-refinement/candidate-recheck-failure-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/failure-fixture-discover-trace.txt`
- `reports/refinement/2026-08-28-harness-refinement/report.md`

## Failure traces and blockers

- `reports/refinement/2026-08-28-harness-refinement/failure-fixture-discover-trace.txt` captures the expected failing-fixture traceback used for the controlled failure-path comparison
- `reports/refinement/2026-08-28-harness-refinement/baseline-failure.json` captures the baseline failing payload without the new rollup field
- `reports/refinement/2026-08-28-harness-refinement/candidate-failure.json` captures the candidate failing payload with the new rollup field
- Blocker encountered: the first parallel baseline failure-path run produced an inconsistent green artifact, so the failure fixture was re-run directly before making the accept/reject decision

## Next hypothesis

Add a `failed_test_trial_spans` rollup so downstream consumers can see each failed test's first/last trial window as a single compact evidence field instead of reconstructing it from separate maps.
