# Measurable Outcomes for Digital Banking Engineering

## From Code Changes to Member and Business Impact at Harbor Federal Credit Union

This executable textbook teaches developers to connect engineering work to measurable technical, operational, member, and business outcomes. **Harbor Federal Credit Union (Harbor FCU) is entirely fictional.** Every member, account, system, transaction, metric, log, incident, and scenario is synthetic; none describes a real institution or person.

> Don't stop at “What did we build?” Ask “What changed, how do we know, and why does it matter?”

## Curriculum status

**Part I, Chapters 0–4, is implemented** as substantive lessons and one coherent measurement lab. **Chapters 5–39 remain planned scaffolds** and structurally intact; their implementation is intentionally deferred. See [the complete contents](CONTENTS.md).

## The outcome chain

```text
Engineering activity → system change → observable metric → measured outcome
                     → member / operational effect → potential business impact
```

An output is what changed, a metric is an observation, and an outcome is measured change. A downstream impact remains *potential* until evidence connects it. For example, a p95 decrease supports “the API became faster under the measured workload”; it does not by itself support “revenue increased.”

## Part I quick start

Python 3.10+ and the standard library are the only requirements. Run from the repository root:

```bash
python3 scripts/introduce_measurement.py
python3 scripts/measure_baseline.py
python3 scripts/choose_metric.py --answer completion_rate
python3 scripts/evaluate_candidate.py
python3 scripts/run_experiment.py
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

## Repository map

- `chapters/` — eight parts and Chapters 0–39.
- `labs/harbor_fcu/` — shared simulation notes.
- `data/synthetic/` — generated or hand-authored fictional observations and provenance.
- `src/harbor_fcu/` — reusable measurement/simulation code.
- `scripts/` — learner-facing commands.
- `tests/` — calculation, scenario, command, and structural checks.
- `docs/` — authoring and data conventions.

## Safety and scope

Never add real member, customer, employee, credential, production, vendor-confidential, or institution-internal information. Part I demonstrates evidence-bounded technical measurement. Production integrations, claims about real institutions, and Chapters 5–39 are out of scope.
