# Chapter 24: Measuring a Backend Optimization

> **Implementation status:** Complete Part V capstone using entirely synthetic data.

## Learning objectives

- Predeclare and automatically evaluate performance, efficiency, correctness, and safety criteria.
- Combine actual timing, plans, deterministic work counters, and normalized-result comparison.
- Write supported conclusions without inventing downstream impact.

## Banking context

Harbor's account-history endpoint makes one account query and a transaction query per account, then processes the results. Volume growth makes this repeated access a justified investigation target.

## Measurable-outcome concept

The baseline and optimized candidates use identical fixtures. Success is declared before evaluation: deterministic modeled p95 is at least 50% lower, queries/request is at most two, normalized results match, and corrected invalid states remain zero. Actual median and p95 are reported but never used as brittle CI gates.

## Planned Harbor FCU scenario

Baseline performs the N+1 pattern without the history index. Optimized performs two set-oriented queries with the composite index. Both results are normalized as sorted JSON and hashed; a mismatch forces correctness and overall status to fail.

## Engineering concept

Instrumentation captures operation, actual duration, query count, rows, result hash, and success. The service-time model is explicitly labeled, deterministic laboratory input. It provides stable criterion evaluation while actual repeated wall-clock timing teaches environmental variation.

## Metrics to measure

Observed median/p95, modeled p95, queries/request, hashes/equivalence, invalid states, and automatic PASS/FAIL. Throughput is useful in Chapter 22 but query efficiency and correctness are the direct capstone outcomes.

## Planned executable exercise

```bash
python3 scripts/run_backend_experiment.py
```

## What to observe and interpretation

The report separates `SUPPORTED CONCLUSION`, `POTENTIAL DOWNSTREAM EFFECT`, and `NOT ESTABLISHED`. Fewer queries and matching results are direct evidence. Observed timing describes this run. Possible member-facing speed is downstream; satisfaction, revenue, and cost savings remain unmeasured.

## Engineering tradeoffs and evidence limitations

The index uses storage and adds write maintenance. The batching query retrieves more transaction rows before retaining five per account. The in-memory, single-process fixture omits real connection pools, production distributions, concurrent writes, network costs, and cache history.

## Automated tests and exercises

Tests deliberately compare normalized candidates, assert query counts and criteria, and avoid arbitrary time thresholds. Exercise: alter one optimized amount and confirm correctness and overall status must fail; propose a production shadow measurement without exposing member data.

## Expected takeaway

Performance improvement without behavioral correctness is not a successful outcome.

## Chapter summary

The Part V experiment improves measured work, preserves behavior, exposes tradeoffs, and limits its claim to the laboratory workload.

## Part transition

Part V established performance and correctness evidence. Part VI asks whether testing, defensive controls, review, and delivery processes preserve those properties through change.

[Previous chapter](chapter-23-finding-backend-bottlenecks-across-layers.md) | [Contents](../../CONTENTS.md) | [Next chapter](../part-06-testing-security-delivery/chapter-25-unit-tests-as-fast-outcome-guardrails.md)
