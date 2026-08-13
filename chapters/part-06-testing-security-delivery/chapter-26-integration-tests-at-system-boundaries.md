# Chapter 26: Measuring Regression Prevention and Defect Escape

> **Synthetic-data notice:** Harbor Federal Credit Union, its releases, users, defects, transfers, and security cases are fictional.

## Learning objectives

- Explain the chapter's engineering control and measured outcome.
- Calculate its deterministic quality metrics.
- Separate observations, supported conclusions, potential effects, and unsupported claims.

## Banking context and engineering concept
A defect is behavior that violates an expectation; a regression breaks behavior that previously worked. Harbor's fictional releases label known validation, query, authorization, and logging defects as detected before deployment or escaped and learned later.

## Measurable-outcome concept
`detection rate = detected before release / total known defects`; `escape rate = escaped / total known defects`. The two partition this fixture, but the denominator includes only defects eventually known. Unknown defects cannot be counted, so the rate is not universal software quality.

## Planned Harbor FCU scenario
Three immutable synthetic release records contain 12 known defects. The analysis calculates totals rather than embedding conclusions and counts escaped defect types so learners can identify the most frequent category.

## Metrics to measure
Known defects, detected pre-release, escaped defects, detection rate, escape rate, and escapes by type. Classification consistency and discovery lag are important limitations.

## Planned executable exercise
```bash
python3 scripts/analyze_defect_escape.py
```
Independently sum known and detected counts, confirm escaped equals their difference, and inspect which type escapes most frequently.

## Interpretation and tradeoffs
The observation supports only a claim about known defects in the defined releases. Earlier detection may reduce production incidents, but no member or financial outcome is established. Adding validation can shift discovery earlier while increasing pipeline duration.

## Automated tests
Tests independently assert the 75% detection rate, 25% escape rate, and logging escape count.

## Exercises
If five defects are found today and an older unknown defect is found tomorrow, which historical denominator changes? Explain why comparing teams with different discovery practices can mislead.

## Expected takeaway

Tests, security controls, and deployment processes are outputs. Their value comes from defined failures detected or prevented and the reliability they help produce; evidence remains bounded to the observed fixtures.

## Chapter summary

The laboratory measures a quality control, preserves a valid-behavior guardrail, and states its limitations. Continue to the next chapter to move one step toward a measured delivery outcome.
