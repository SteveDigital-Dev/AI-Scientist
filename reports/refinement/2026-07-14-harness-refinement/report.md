# Nightly Harness Refinement Report

Date: 2026-07-14
Repo: `D:\GitHub\AI-Scientist`
Scope: `tests/benchmark_runner.py` reuse-discovery isolation
Decision: Accept and apply
Success signal: Improved repeated-trial reliability from 20% to 100% on the fixed stateful benchmark with no critical regression on the smoke benchmark

## Hypothesis

`--reuse-discovery` claims it discovers once and deep-copies the suite per trial, but the implementation was reusing the same discovered test objects. Cloning the discovered suite for each trial should remove cross-trial state leakage while preserving the benefit of skipping re-discovery.

## Fixed benchmark set

1. CLI smoke benchmark
   - Command artifact: `reports/refinement/2026-07-14-harness-refinement/baseline-cli-smoke.json`
   - Candidate artifact: `reports/refinement/2026-07-14-harness-refinement/candidate-cli-smoke.json`
2. Stateful reuse benchmark
   - Command artifact: `reports/refinement/2026-07-14-harness-refinement/baseline-stateful.json`
   - Candidate artifact: `reports/refinement/2026-07-14-harness-refinement/candidate-stateful.json`
   - Failure trace: `reports/refinement/2026-07-14-harness-refinement/baseline-stateful-failure-trace.txt`

## Candidate

Accepted candidate:
- `reuse-discovery-deepcopy`
  - Change: deep-copy the discovered unittest suite before each warmup/trial run
  - Files: `tests/benchmark_runner.py`, `tests/test_benchmark_runner.py`, `tests/test_reuse_discovery_fixture.py`

Failed candidates:
- None generated this cycle

## Baseline vs candidate

### Stateful reuse benchmark

- Baseline: 1/5 successful, 4/5 failed, pass rate `0.20`, error rate `0.80`, avg latency `0.007074s`, throughput `141.36 trials/s`
- Candidate: 5/5 successful, 0/5 failed, pass rate `1.00`, error rate `0.00`, avg latency `0.000871s`, throughput `1147.87 trials/s`
- Quality delta: `+4` successful trials
- Reliability delta: pass rate `+0.80`, error rate `-0.80`
- Latency delta: `-0.006203s` average, `-87.69%`
- Throughput delta: `+1006.51 trials/s`, `+712.03%`

### CLI smoke benchmark

- Baseline: 5/5 successful, pass rate `1.00`, avg latency `0.000872s`, throughput `1147.00 trials/s`
- Candidate: 5/5 successful, pass rate `1.00`, avg latency `0.000557s`, throughput `1795.01 trials/s`
- Quality delta: no change
- Reliability delta: no change
- Latency delta: `-0.000315s` average, `-36.10%`
- Throughput delta: `+648.01 trials/s`, `+56.50%`
- Note: this is a microbenchmark and likely contains run-to-run noise, but there was no slowdown or reliability loss.

## Failure trace / blocker evidence

- Baseline blocker: repeated suite reuse leaked instance state between trials.
- Trace excerpt source: `reports/refinement/2026-07-14-harness-refinement/baseline-stateful-failure-trace.txt`
- Symptom: second run failed with `AssertionError: True is not false` after the fixture detected `_seen` persisted across trials.

## Validation

- `python tests/benchmark_runner.py --start-dir tests --pattern test_cli_smoke_fixture.py --trials 5 --warmup 1 --reuse-discovery --output reports/refinement/2026-07-14-harness-refinement/candidate-cli-smoke.json`
- `python tests/benchmark_runner.py --start-dir reports/refinement/2026-07-14-harness-refinement/baseline-fixture --pattern test_stateful_fixture.py --trials 5 --warmup 0 --reuse-discovery --output reports/refinement/2026-07-14-harness-refinement/candidate-stateful.json`
- `python -m unittest tests.test_benchmark_runner`

## Touched files

- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `tests/test_reuse_discovery_fixture.py`
- `reports/refinement/2026-07-14-harness-refinement/report.md`

## Generated artifacts

- `reports/refinement/2026-07-14-harness-refinement/baseline-fixture/test_stateful_fixture.py`
- `reports/refinement/2026-07-14-harness-refinement/baseline-cli-smoke.json`
- `reports/refinement/2026-07-14-harness-refinement/baseline-stateful.json`
- `reports/refinement/2026-07-14-harness-refinement/baseline-stateful-failure-trace.txt`
- `reports/refinement/2026-07-14-harness-refinement/candidate-cli-smoke.json`
- `reports/refinement/2026-07-14-harness-refinement/candidate-stateful.json`
- `reports/refinement/2026-07-14-harness-refinement/report.md`

## Next hypothesis

Add an optional benchmark payload field for captured failure summaries so rejected candidates and flaky benchmarks keep first-order failure evidence without requiring a separate repro command.
