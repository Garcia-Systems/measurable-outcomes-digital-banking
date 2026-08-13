# Chapter 23: Finding Backend Bottlenecks Across Layers

> **Scaffold status:** Planned chapter; lesson and full lab are intentionally deferred.

## Learning objectives

- Decompose request time.
- Use traces to prioritize bottlenecks.

## Measurable-outcome concept

End-to-end latency attribution.

## Planned Harbor FCU scenario

In the entirely fictional Harbor FCU simulation, learners will trace a slow account-dashboard request through application, database, and vendor calls.

## Metrics to measure

- Span duration.
- Critical-path share.
- End-to-end latency.

## Planned executable exercise

Aggregate synthetic traces and identify the largest critical-path component.

## Expected takeaway

Optimize the measured constraint rather than the most visible component.
