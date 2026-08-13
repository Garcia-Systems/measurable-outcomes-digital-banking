# Part I synthetic observations

These three CSV files contain deterministic, invented observations for the fictional Harbor FCU member-verification service. No row represents a person, account, transaction, or real institution. Each window contains 20 requests under the same synthetic workload and uses UTC timestamps. `verification_baseline.csv` is the starting window; `verification_fast_candidate.csv` is deliberately fast but unreliable; and `verification_reliable_candidate.csv` is the controlled after window. The files are committed rather than randomly regenerated so every learner obtains the same result.

Schema: `timestamp` (UTC ISO-8601), `operation`, `successful` (`true`/`false`), and non-negative `latency_ms`.
