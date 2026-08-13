# Measurable Outcomes for Digital Banking Engineering

## From Code Changes to Member and Business Impact at Harbor Federal Credit Union

This executable textbook teaches developers to connect engineering work to measurable technical, operational, member, and business outcomes. **Harbor Federal Credit Union (Harbor FCU) is entirely fictional.** Every member, account, system, transaction, metric, log, incident, and scenario is synthetic; none describes a real institution or person.

> Don't stop at “What did we build?” Ask “What changed, how do we know, and why does it matter?”

## Curriculum status

**Parts I–V, Chapters 0–24, are implemented** as substantive lessons and coherent measurement labs. **Chapters 25–39 remain planned scaffolds** and structurally intact; their implementation is intentionally deferred. See [the complete contents](CONTENTS.md).

## The outcome chain

```text
Engineering activity → system change → observable metric → measured outcome
                     → member / operational effect → potential business impact
```

An output is what changed, a metric is an observation, and an outcome is measured change. A downstream impact remains *potential* until evidence connects it. For example, a p95 decrease supports “the API became faster under the measured workload”; it does not by itself support “revenue increased.”

## Parts I–V quick start

Python 3.10+ and the standard library are the only requirements. Run from the repository root:

```bash
python3 scripts/introduce_measurement.py
python3 scripts/measure_baseline.py
python3 scripts/choose_metric.py --answer completion_rate
python3 scripts/evaluate_candidate.py
python3 scripts/run_experiment.py
python3 scripts/measure_completion.py
python3 scripts/analyze_funnel.py
python3 scripts/analyze_completion_time.py
python3 scripts/compare_experience.py
python3 scripts/classify_claims.py
python3 scripts/measure_api_reliability.py
python3 scripts/analyze_api_latency.py
python3 scripts/simulate_retries.py
python3 scripts/compare_integrations.py
python3 scripts/run_integration_experiment.py
python3 scripts/measure_reliability.py
python3 scripts/explore_observability.py
python3 scripts/investigate_incident.py
python3 scripts/measure_incident_response.py
python3 scripts/run_reliability_experiment.py
python3 scripts/measure_query_performance.py
python3 scripts/compare_database_index.py
python3 scripts/analyze_backend_workload.py
python3 scripts/simulate_backend_concurrency.py
python3 scripts/run_backend_experiment.py
python3 -m unittest discover -s tests -v
```

The labs reuse committed observations in `data/synthetic/part1`. Results are deterministic. The deliberately fast Chapter 3 candidate reports overall `FAIL` because it violates reliability guardrails; that is a successful experiment, not a command failure.

## What Part I provides

- Reusable loaders, nearest-rank percentiles, rates, comparisons, and threshold evaluation in `src/harbor_fcu/measurement.py`.
- A small structured measurement report that later Parts can extend.
- Matched verification baseline, unsafe fast candidate, and reliable candidate scenarios.
- Conceptual and executable exercises with answer keys in each chapter.
- Automated calculation, scenario, CLI, curriculum, and Markdown-link checks.

The original `python3 scripts/measure_api_baseline.py` exercise remains available for compatibility.

Part II extends the same utilities with deterministic digital-application events, task completion, funnel conversion and abandonment, median/p95 and stage timing, controlled before/after criteria, and evidence-strength classification. Regenerate its committed observations with `python3 scripts/generate_member_journey.py`.

Part III adds network-free fictional integrations: ClearVerify REST member verification, HeritageCore SOAP core lookup, and a minimal NorthstarPay idempotency example. Harbor-owned adapters normalize protocol outcomes into shared telemetry; laboratories measure reliability, latency tails, retry recovery and cost, adapter comparability, and declared before/after criteria.

Part IV adds deterministic application requests, component timing, structured privacy-conscious logs, correlated request/operation identifiers, health evidence, alert windows, and incident records. Its five laboratories measure useful-work availability, endpoint reliability, alert sensitivity and false positives, chronological incident diagnosis, MTTD/MTTR, and a predeclared before/after incident-response experiment. In this repository MTTD is incident start to detection, while MTTR is incident start to useful-service restoration.

Part V adds an in-memory deterministic SQLite fixture, repeated query timing, query-plan inspection, an index before/after experiment, backend component/workload analysis, N+1 query-count instrumentation, concurrency and idempotency guardrails, normalized result hashing, and a predeclared optimization capstone. Wall-clock values are educational observations; deterministic plans, work counters, modeled workload values, and correctness checks keep CI portable.

## Repository map

- `chapters/` — eight parts and Chapters 0–39.
- `labs/harbor_fcu/` — shared simulation notes.
- `data/synthetic/` — generated or hand-authored fictional observations and provenance.
- `src/harbor_fcu/` — reusable measurement/simulation code.
- `scripts/` — learner-facing commands.
- `tests/` — calculation, scenario, command, and structural checks.
- `docs/` — authoring and data conventions.

## Safety and scope

Never add real member, customer, employee, credential, production, vendor-confidential, or institution-internal information. Parts I–V demonstrate evidence-bounded technical, member-experience, integration, incident-response, database, and backend measurement. Production integrations, claims about real institutions, and Chapters 25–39 are out of scope.
