# Measurable Outcomes for Digital Banking Engineering

## From Code Changes to Member and Business Impact at Harbor Federal Credit Union

This executable textbook teaches developers to connect engineering work to measurable technical, operational, member, and business outcomes. **Harbor Federal Credit Union (Harbor FCU) is entirely fictional.** Every member, account, system, transaction, metric, log, incident, and scenario is synthetic; none describes a real institution or person.

> **Don't stop at “What did we build?” Ask “What changed, how do we know, and why does it matter?”**

## Curriculum status

**All eight Parts and all 40 chapters (0–39) are complete**, with substantive lessons, deterministic laboratories, and a final cross-layer engineering review. See [the complete contents](CONTENTS.md).

## The outcome chain

```text
Engineering activity → engineering output → observable metric → measured outcome
                     → member / operational effect → business relevance
```

An output is what changed, a metric is an observation, and an outcome is measured change. A downstream impact remains *potential* until evidence connects it. For example, a p95 decrease supports “the API became faster under the measured workload”; it does not by itself support “revenue increased.”

The chapters repeatedly apply one engineering loop: **DEFINE → MEASURE → BUILD → OBSERVE → COMPARE → LEARN → IMPROVE → COMMUNICATE**. Later Parts reuse the definitions and evidence discipline established in Part I rather than redefining them.

## Learner quick-start

### Requirements

Python 3.10+, Bash, Git, and the Python standard library are the only requirements. No package installation, credentials, network service, database server, or AI service is needed. Clone the repository, enter its root, and confirm Python with `python3 --version`.

### Run the first laboratory

```bash
python3 scripts/introduce_measurement.py
```

Read [Chapter 0](chapters/part-01-foundations/chapter-00-from-code-to-outcomes.md), predict the output, run the command, and answer the chapter exercises before checking its answer key. Then follow each chapter's **Next chapter** link through [the complete contents](CONTENTS.md). The sequence deliberately moves from definitions and baselines, through member and system layers, to evidence-bounded business communication.

### Validate your environment and progress

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_structure.py
./scripts/validate-labs.sh
```

The test command checks calculations, scenarios, commands, curriculum structure, and Markdown links. The structure command gives a concise book-integrity result. The laboratory runner executes exactly one documented command for each Chapter 0–39, in order, and stops visibly on failure. Laboratories reuse committed or generated synthetic observations and are deterministic except for explicitly labeled local wall-clock observations in Part V; Part V decisions use portable query plans, work counts, modeled values, and result equivalence instead.

### Run the capstone

After completing Parts I–VIII, run:

```bash
python3 scripts/run_capstone.py
```

Audit its values back to their deterministic fixture and separate supported conclusions, hypotheses, and not-established claims. The [glossary](docs/GLOSSARY.md), [metrics reference](docs/METRICS_REFERENCE.md), and [Harbor architecture](docs/HARBOR_ARCHITECTURE.md) are quick references while you work.

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

Part VI adds regression-detection experiments, known-defect detection and escape rates, defensive transfer and safe-logging fixtures, a local release-readiness gate, and a predeclared before/after delivery experiment. The improved synthetic pipeline catches more defined defects at the cost of longer validation; this supports bounded quality claims, not claims of complete security or production infallibility. See the [Part VI laboratory guide](labs/harbor_fcu/part-06-testing-security-delivery.md).

Part VII reuses Harbor API, vendor, database, deployment, alert, and incident telemetry for descriptive grouping, baseline anomaly detection, capacity forecasting, and explainable incident scoring. It compares rules and scoring on identical ground truth, then measures the downstream investigation queue, MTTD, and MTTR in a controlled simulation. The implementation is standard-library only: it demonstrates that predictions are inputs to action—not business outcomes—and does not require an external AI service. See the [Part VII laboratory guide](labs/harbor_fcu/part-07-analytics-automation-ml.md).

Part VIII connects the technical evidence to measured member and operational behavior, explicitly labels measured/derived/assumed/estimated values, and renders quantitative reports for engineers, operations, and executives. Its capstone reviews the synthetic Digital Account Opening Improvement across technical, reliability, delivery, member, operational, and business-relevance layers. See the [Part VIII laboratory guide](labs/harbor_fcu/part-08-business-impact.md).

## Final capstone

Run `python3 scripts/run_capstone.py`. The criteria are declared in code before evaluation, all report values originate in the executable synthetic environment, and unsupported satisfaction, revenue, retention, causality, and realized-savings claims remain explicit non-claims.

## Repository map

- `chapters/` — eight parts and Chapters 0–39.
- `labs/harbor_fcu/` — shared simulation notes.
- `data/synthetic/` — generated or hand-authored fictional observations and provenance.
- `src/harbor_fcu/` — reusable measurement/simulation code.
- `scripts/` — learner-facing commands.
- `tests/` — calculation, scenario, command, and structural checks.
- `docs/` — terminology, metric, architecture, authoring, and data references.
- `scripts/validate-labs.sh` — all 40 laboratories in curriculum order.
- `scripts/validate_structure.py` — Parts, chapters, contents, and local-link integrity.

## Safety and scope

Never add real member, customer, employee, credential, production, vendor-confidential, or institution-internal information. Harbor FCU, ClearVerify, HeritageCore, NorthstarPay, and all other vendors are fictional; all member, account, transaction, operational, and financial observations are synthetic. No laboratory contacts an external financial system or AI service. The completed book demonstrates evidence-bounded technical, member, operational, and business-relevance measurement; production integrations and claims about real institutions remain out of scope.
