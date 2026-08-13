# Metrics quick reference

Every metric needs a population, window, unit, filters, and edge-case rule. A metric describes its layer; it does not automatically prove the next link in the outcome chain.

| Layer | Metric | Basic calculation or definition | Does **not** prove |
|---|---|---|---|
| Technical | Latency (median, p95) | Elapsed operation time; this book uses nearest-rank percentiles | Completion, satisfaction, or causality |
| Technical | Error rate | failed eligible operations / eligible operations × 100 | Why failures occurred or member harm |
| Technical | Throughput | completed operations / measured time | Correctness or capacity beyond tested load |
| Technical | Query count | database statements per defined operation | That fewer queries are faster on every machine |
| Reliability | Availability | useful-service opportunities / defined opportunities × 100 | Every endpoint or member journey was available |
| Reliability | MTTD | mean(detection − incident start) | Detection quality outside the incident set |
| Reliability | MTTR | mean(restoration − incident start) | Prevention, root-cause removal, or financial effect |
| Member experience | Completion rate | completed eligible starts / eligible starts × 100 | Satisfaction, adoption, or account opening unless those are separately defined |
| Member experience | Abandonment rate | incomplete eligible starts / eligible starts × 100 | The reason a task stopped |
| Member experience | Time to complete | completion timestamp − start timestamp for the declared population | Experience of excluded abandoners |
| Delivery | Defect detection rate | known defects caught before boundary / known defects introduced × 100 | Absence of unknown defects |
| Delivery | Defect escape rate | known defects crossing boundary / known defects introduced × 100 | Production incident probability |
| Delivery | Release success | releases meeting declared validation/result criteria / eligible releases × 100 | Future release safety |
| ML / analytics | Precision | true positives / (true positives + false positives) | Operational value or low missed-incident cost |
| ML / analytics | Recall | true positives / (true positives + false negatives) | Low investigation burden |
| ML / analytics | Forecast error | e.g. mean absolute error between forecast and actual | That acting on the forecast improves an outcome |
| Operations | Manual review count | reviews in a declared population/window | Labor savings without time and cost evidence |
| Operations | Investigation time | investigation end − investigation start | Causal attribution to a tool without a valid comparison |
| Business | Measured cost | directly observed expense with provenance | Avoidable or realized savings |
| Business | Estimated value | measured/derived quantities combined with explicit assumptions | Booked savings, revenue, ROI, or causal impact |

See the concise definitions in the [glossary](GLOSSARY.md) and the executable formulas in `src/harbor_fcu/measurement.py`.
