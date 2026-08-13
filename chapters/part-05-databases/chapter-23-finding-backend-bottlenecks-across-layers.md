# Chapter 23: Correctness, Concurrency, and Performance

> **Implementation status:** Complete. This is an educational reservation, not a banking ledger.

## Learning objectives

- Explain transaction boundaries, atomicity, locking, consistency, and lost updates.
- Apply idempotency from Chapter 12 to state-changing operations.
- Treat correctness as a nonnegotiable performance guardrail.

## Banking context

Two synthetic requests see $500 available. A requests $350 and B requests $250. If both authorize against the same stale snapshot, total reservations reach $600. A superficially fast check has produced an invalid state.

## Measurable-outcome concept

`FAST + WRONG = FAILURE`. Targets must combine performance with zero invalid final states and zero duplicate state changes. Lower latency cannot compensate for violated money-state invariants.

## Planned Harbor FCU scenario

The careless simulation separates reads from decisions and records one oversubscribed state. The corrected simulation serializes the check-and-reserve decision conceptually: A succeeds, B is rejected, $150 remains. Replaying A's idempotency key changes state zero additional times.

## Engineering concept

A transaction boundary makes related work atomic: all or none. Locking or a conditional update prevents concurrent decisions from both using stale availability. Consistency means invariants hold at commit. Idempotency prevents retried requests from applying twice; it does not replace concurrency control.

## Metrics to measure

Invalid final states, accepted operations, remaining amount, and duplicate state changes. A real system would also measure lock wait, conflict/retry rate, p95, and throughput.

## Planned executable exercise

```bash
python3 scripts/simulate_backend_concurrency.py
```

## What to observe and interpretation

The corrected outcome has zero invalid states and zero duplicate changes. It demonstrates the algorithmic guardrail deterministically, not SQLite's production concurrency behavior.

## Engineering tradeoffs and evidence limitations

Stronger serialization can increase waits and reduce throughput. Optimistic approaches can increase retries. Select a mechanism using contention and correctness evidence; never weaken the invariant to win a benchmark.

## Automated tests and exercises

Tests assert the careless invalid state, corrected nonnegative result, and idempotent replay. Exercise: reverse operation order and state the valid outcomes; add a p95 target but explain why arbitrary CI timing must not gate it.

## Expected takeaway

Performance criteria are incomplete without transaction, consistency, and duplicate-operation guardrails.

## Chapter summary

Correctness defines success; concurrency and idempotency protect it under competing and repeated work.

[Previous chapter](chapter-22-throughput-concurrency-and-saturation.md) | [Contents](../../CONTENTS.md) | [Next chapter](chapter-24-proving-performance-improvements-hold.md)
