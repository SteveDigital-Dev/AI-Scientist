# Harness Refinement Report — 2026-05-29

## Scope
Nightly local harness refinement in `D:\GitHub\AI-Scientist`.

## Tool availability
- `opencode --version` → available
- `pi --version` → available

## Baseline (fixed benchmark, >=3 trials)
Command:
`python tests/benchmark_runner.py --trials 5 --warmup 1 --reuse-discovery`

Results:
- pass_rate: **1.0**
- error_rate: **0.0**
- avg_seconds: **0.00282498**
- stdev_seconds: **0.00006276**

## Candidate hypothesis
Replace `copy.deepcopy(discovered_suite)` per trial with a lightweight blueprint-based test suite reconstruction (`TestCaseClass(method_name)` list) to reduce cloning overhead.

## Candidate results (>=3 trials)
Same benchmark command after candidate edit:
- pass_rate: **1.0**
- error_rate: **0.0**
- avg_seconds: **0.00307988**
- stdev_seconds: **0.00009593**

## Comparison
- Reliability: no regression (pass_rate unchanged at 100%)
- Throughput/latency: **worse**
  - avg latency delta: **+9.02%** (0.00282498 → 0.00307988)

## Decision
**Rejected candidate** (did not meet apply threshold; latency regressed and no quality gain).

## Revert status
Candidate change was reverted. Verification rerun:
`python tests/benchmark_runner.py --trials 3 --warmup 1 --reuse-discovery`
- pass_rate: **1.0**
- avg_seconds: **0.00316387**

## Files touched
- `tests/benchmark_runner.py` (temporary candidate edit, then reverted)

## Git/commit status
Could not create commit because this path is **not initialized as a git worktree** (`fatal: not a git repository`).

## Next hypothesis
Profile `run_once` internals (discovery/clone/runner split timing) and target only the dominant sub-step, then retest with the same fixed benchmark command.
