# Measurable Outcomes for Digital Banking Engineering

## From Code Changes to Member and Business Impact at Harbor Federal Credit Union

This executable textbook teaches full-stack developers to connect engineering work to measurable technical, operational, member, and business outcomes. **Harbor Federal Credit Union (Harbor FCU) is entirely fictional.** Its members, systems, metrics, architecture, and results are synthetic teaching material created for this repository; they do not represent any real credit union or person.

> **Don't stop at “What did we build?” Ask “What changed, how do we know, and why does it matter?”**

## The outcome chain

Every lab uses the same reasoning model:

**Engineering activity → system change → observable metric → member/operational effect → business outcome**

An **output** is what was built or changed. A **metric** is an observation. An **outcome** is the measured improvement. **Impact** explains why that improvement matters. For example:

| Layer | Example |
|---|---|
| Output | Optimized a database query |
| Metric | p95 query latency |
| Baseline | 820 ms |
| After | 135 ms |
| Outcome | Faster data retrieval |
| Potential impact | Faster member-facing workflows and reduced infrastructure load |

The last statement is deliberately a *potential* impact until evidence connects the technical change to member or business results. The book distinguishes correlation from causation and never treats a plausible benefit as a proven one.

## One evolving, executable lab

Across eight parts and 40 chapters (0–39), learners evolve one local Harbor FCU simulation. Its generated datasets will cover fictional members, accounts, transactions, sessions, funnels, APIs, integrations, queries, logs, errors, incidents, tests, deployments, and analytics events. Exercises follow one loop:

```text
Observe baseline → Identify problem → Make engineering change
→ Run experiment/test → Measure again → Compare → Explain outcome
```

The curriculum progresses from measurement foundations, through member experience, integrations, reliability, databases, testing/security/delivery, and grounded analytics/ML, to responsible business communication. See [the complete contents](CONTENTS.md). Chapter files are intentionally concise implementation briefs: later work will turn them into lessons without creating 40 disconnected applications.

## Quick start: measure a baseline

Python 3.10+ is the only requirement for the initial exercise; it uses the standard library.

```bash
python3 scripts/measure_api_baseline.py
python3 -m unittest discover -s tests -v
```

The first command reads synthetic API observations from `data/synthetic/api_requests.csv` and reports request count, success rate, mean latency, and p95 latency. This is an observation, not evidence that a particular engineering change caused an outcome.

## Expected technology

Later labs will add Python measurement, simulation, and lightweight ML; SQL/MySQL-compatible database exercises; PHP REST/SOAP and server-side examples; JavaScript/TypeScript, HTML, and CSS member experiences; and command-line automated tests. Labs remain local, small, and free of paid cloud services, proprietary banking systems, and real financial data.

## Repository map

- `chapters/` — eight numbered parts and 40 chapter briefs.
- `labs/harbor_fcu/` — the shared simulation's fixtures and future lab modules.
- `data/synthetic/` — generated, fictional data only.
- `src/harbor_fcu/` — reusable simulation and measurement code.
- `scripts/` — learner-facing commands.
- `tests/` — executable and structural checks.
- `docs/` — authoring and data conventions for future chapters.

## Safety and scope

Never add real member, customer, employee, credential, production, vendor-confidential, or institution-internal data. Synthetic identifiers must be obviously fictional. This scaffold designs the complete curriculum and proves its execution pattern; full lessons, production integrations, and later-chapter exercises are intentionally deferred.
