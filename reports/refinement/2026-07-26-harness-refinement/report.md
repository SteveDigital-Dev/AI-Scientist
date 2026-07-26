# Harness Refinement Report

Date: 2026-07-26
Repo: `D:\GitHub\AI-Scientist`
Decision: Accept candidate and commit
Success signal: Candidate passed the fixed benchmark set in 5/5 trials

## Hypothesis

The benchmark harness is leaking `unittest.defaultTestLoader` state and discovered temp-fixture modules across repeated in-process runs on Windows. Replacing process-global discovery with a fresh `unittest.TestLoader()` per discovery and cleaning up newly imported test modules after each discovery/run should eliminate the cross-drive loader failure and temp-fixture import contamination.

## Fixed benchmark set

Measured with `measure_benchmark_runner.py` over 5 trials:

1. `cli_smoke`
2. `default_loader_isolation`
3. `repeated_temp_fixture`

## Baseline vs candidate

Baseline artifacts:
- `reports/refinement/2026-07-26-harness-refinement/baseline.json`
- `reports/refinement/2026-07-26-harness-refinement/baseline-failure-trace.txt`

Candidate artifacts:
- `reports/refinement/2026-07-26-harness-refinement/candidate.json`
- `reports/refinement/2026-07-26-harness-refinement/candidate-failure-trace.txt`

Measured deltas:
- Quality delta: benchmark-set pass rate improved from `0.0` to `1.0` (`+1.0`)
- Reliability delta: error rate improved from `1.0` to `0.0` (`-1.0`)
- Reliability delta: failed trials improved from `5/5` to `0/5`
- Latency delta: average trial time increased from `0.0721s` to `0.1429s` (`+0.0709s`)
- Throughput delta: dropped from `13.8770` to `6.9957` trials/sec (`-6.8813`)

## Failure evidence

Baseline first-order failures:
- `default_loader_isolation`: `ValueError: path is on mount 'D:', start on mount 'C:'`
- `repeated_temp_fixture`: `ImportError` from cached `test_failure_fixture` imports pointing at prior temp directories
- After the first contaminated trial, even `cli_smoke` began failing due to leaked loader state

Failure traces:
- `reports/refinement/2026-07-26-harness-refinement/baseline-failure-trace.txt`
- `reports/refinement/2026-07-26-harness-refinement/candidate-failure-trace.txt`

## Candidate summary

Accepted candidate:
- `tests/benchmark_runner.py`
  - use a fresh `unittest.TestLoader()` for each discovery
  - invalidate import caches before discovery
  - remove newly imported test modules under the discovered start directory after discovery/run
- `tests/test_benchmark_runner.py`
  - add regression coverage for repeated temp-fixture runs
  - add regression coverage for leaked `_top_level_dir` state on the process-global default loader

Failed candidates:
- None in this cycle

## Validation

- `python -m unittest tests.test_benchmark_runner -v`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label baseline --module-path reports/refinement/2026-07-26-harness-refinement/artifacts/baseline/benchmark_runner.py --output reports/refinement/2026-07-26-harness-refinement/baseline.json --failure-trace reports/refinement/2026-07-26-harness-refinement/baseline-failure-trace.txt --trials 5`
- `python reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py --label candidate --module-path tests/benchmark_runner.py --output reports/refinement/2026-07-26-harness-refinement/candidate.json --failure-trace reports/refinement/2026-07-26-harness-refinement/candidate-failure-trace.txt --trials 5`

## Touched files

- `tests/benchmark_runner.py`
- `tests/test_benchmark_runner.py`
- `reports/refinement/2026-07-26-harness-refinement/measure_benchmark_runner.py`
- `reports/refinement/2026-07-26-harness-refinement/report.md`

## Next hypothesis

If this harness needs both reliability hardening and lower overhead, the next reversible experiment should target the added module-cleanup cost directly, for example by narrowing cleanup to discovered test module names instead of all modules imported from the start directory.
