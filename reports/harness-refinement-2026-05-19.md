# AI Scientist Harness Refinement Report — 2026-05-19

## Scope
Nightly local harness refinement in `D:\GitHub\AI-Scientist`.

## Baseline
Command:
`python tests/benchmark_runner.py --trials 3 --warmup 1 --reuse-discovery`

Metrics (3 trials):
- Avg latency: **0.003624 s**
- Stdev latency: 0.000066 s
- Pass rate: **100%**
- Error rate: **0%**

## Candidate Hypothesis
Disable suite reuse/discovery caching to test whether fresh discovery each trial improves reliability without harming speed.

Candidate command:
`python tests/benchmark_runner.py --trials 3 --warmup 1 --no-reuse-discovery`

Metrics (3 trials):
- Avg latency: **0.005108 s**
- Stdev latency: 0.000093 s
- Pass rate: **100%**
- Error rate: **0%**

## Comparison
- Latency change: **+40.94% slower** (`0.003624s -> 0.005108s`)
- Throughput change: **-29.06%**
- Reliability: no change (100% pass, 0% errors)

## Decision
**REJECT** candidate.

Reason: Candidate does not meet apply threshold (needs >=5% quality gain OR >=10% throughput/latency gain with no critical reliability regression). It regressed speed materially and offered no reliability gain.

## Diffs Touched
- No code/config files changed.
- Report added:
  - `reports/harness-refinement-2026-05-19.md`

## Commit Status
- Not committed (repository has no `.git` metadata in current directory).
- Fallback plan: once repo metadata is restored, commit report/history artifacts and continue reversible code-level experiments.

## Next Hypothesis
Test a low-overhead benchmark execution path that keeps current `--reuse-discovery` behavior but reduces per-trial runner overhead (e.g., stream handling/runner lifecycle) and validate against current baseline.