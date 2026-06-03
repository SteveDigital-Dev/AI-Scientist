# Harness Refinement Report — 2026-05-28

## Scope
Nightly local harness refinement in `D:\GitHub\AI-Scientist`.

## Tool availability
- `opencode --version` → `1.1.23`
- `pi --version` → `0.58.1`

## Baseline (fixed benchmark, >=3 trials)
Command:
`python tests/benchmark_runner.py --trials 5 --warmup 1 --reuse-discovery`

Results:
- pass_rate: **1.0**
- error_rate: **0.0**
- avg_seconds: **0.00282492**
- stdev_seconds: **0.00004310**

## Candidate hypothesis
Replace per-trial `copy.deepcopy(discovered_suite)` cloning with test-id based reload (`loadTestsFromNames`) to reduce benchmark harness overhead.

## Candidate results (>=3 trials)
Same benchmark command after candidate edit:
- pass_rate: **1.0**
- error_rate: **0.0**
- avg_seconds: **0.00521310**
- stdev_seconds: **0.00014034**

## Comparison
- Reliability: no regression (pass_rate unchanged at 100%)
- Throughput/latency: **worse**
  - avg latency delta: **+84.54%** (0.00282492 → 0.00521310)

## Decision
**Rejected candidate** (did not meet apply threshold; performance regressed).

## Revert status
Candidate change was reverted. Verification rerun:
`python tests/benchmark_runner.py --trials 3 --warmup 1 --reuse-discovery`
- pass_rate: **1.0**
- avg_seconds: **0.00311750**

## Files touched
- `tests/benchmark_runner.py` (temporary candidate edit, then reverted)

## Git/commit status
Could not create commit because this path is **not initialized as a git worktree** (`fatal: not a git repository`).

## Next hypothesis
Try micro-optimizing the current deepcopy path (e.g., custom lightweight suite clone that preserves object shape without full deep object traversal), then re-benchmark with the same fixed trial setup.
