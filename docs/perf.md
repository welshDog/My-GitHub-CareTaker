# Performance Benchmarks

## Method
- Use cached GraphQL repo listing
- Duplicate scan computes pairwise similarity with heuristics
- Redis caches results to avoid repeat cost

## Target
- Repositories up to 10GB: recommend running scans with metadata-only mode; code-level diff disabled.

## Results (example)
- 100 repos, median scan ~1.2s with cache warm
- 500 repos, ~6.5s
-
## Free-side switch
- If GitHub limits exceeded or token missing, fall back to local metadata and user-provided repo lists.
