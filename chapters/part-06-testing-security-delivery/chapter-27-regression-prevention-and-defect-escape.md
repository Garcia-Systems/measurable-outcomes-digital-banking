# Chapter 27: Measuring Secure Coding Controls

> **Synthetic-data notice:** Harbor Federal Credit Union, its releases, users, defects, transfers, and security cases are fictional.

## Learning objectives

- Explain the chapter's engineering control and measured outcome.
- Calculate its deterministic quality metrics.
- Separate observations, supported conclusions, potential effects, and unsupported claims.

## Banking context and engineering concept
Transfer boundaries must validate amount, required fields, operation enums, and authorization. Output handling must avoid synthetic secrets in telemetry. Authentication establishes identity; authorization decides permitted action. They are separate boundaries. Dependency risk and secrets management remain conceptual here—no offensive tooling or live dependency is used.

## Measurable-outcome concept
“Added validation” is an output. The stronger observation reports defined invalid cases tested, correctly rejected, incorrectly accepted, valid fixtures accepted, and prohibited values found in logs. A finite suite measures those cases only; it cannot establish that an application is secure.

## Planned Harbor FCU scenario
Reusable fixtures include a valid transfer, negative/zero/oversized/missing amounts, an unexpected operation, and an unauthorized operation. An unsafe logger includes a fictional token. The safe logger allowlists operational fields, linking secure output handling to Chapter 16's observability lesson.

## Metrics to measure
Security-case pass rate, invalid cases rejected, invalid cases accepted, valid guardrails, and sensitive-data exposures detected. All identifiers and values are explicitly synthetic.

## Planned executable exercise
```bash
python3 scripts/run_security_validation.py
```
Observe that the scanner finds the prohibited fixture in unsafe output and finds none in allowlisted output. Safe output should retain request and operation context without the prohibited value.

## Interpretation and tradeoffs
More logging can improve diagnosis but increase exposure. Omission reduces exposure while potentially reducing context; define permitted fields and diagnostic needs. Passing says only that the defined validation cases passed—not that all threats, dependencies, authentication paths, or future inputs are safe.

## Automated tests
Tests cover validation boundaries, authorization, exposure detection, and redaction by omission. They intentionally avoid universal-security assertions.

## Exercises
Add a valid boundary value of 10,000 and an invalid value just above it. Which requirement justifies the threshold? What evidence would be needed before changing it?

## Expected takeaway

Tests, security controls, and deployment processes are outputs. Their value comes from defined failures detected or prevented and the reliability they help produce; evidence remains bounded to the observed fixtures.

## Chapter summary

The laboratory measures a quality control, preserves a valid-behavior guardrail, and states its limitations. Continue to the next chapter to move one step toward a measured delivery outcome.

[Previous chapter](chapter-26-integration-tests-at-system-boundaries.md) | [Contents](../../CONTENTS.md) | [Next chapter](chapter-28-secure-inputs-and-measurable-risk-reduction.md)
