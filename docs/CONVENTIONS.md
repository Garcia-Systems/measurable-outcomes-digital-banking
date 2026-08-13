# Authoring and lab conventions

## Narrative conventions

- Always call the institution **Harbor Federal Credit Union (Harbor FCU)** and identify it as fictional when context could be ambiguous.
- Use the outcome chain: output → metric → outcome → impact.
- State the baseline, measurement window, population, target, and limitations.
- Label unsupported downstream benefits as hypotheses or potential impacts. Correlation alone does not establish causation.
- Extend the shared simulation rather than creating a standalone chapter application.

## Chapter convention

Chapter files live under `chapters/part-NN-name/chapter-NN-slug.md`, use chapter numbers 0–39, and retain the seven scaffold headings. An implemented chapter should add prerequisites, lesson material, an executable lab, interpretation questions, and verification while preserving its planned scope.

## Code and data convention

- Python commands run from the repository root and should prefer the standard library unless a dependency is justified.
- Reusable logic belongs in `src/harbor_fcu`; thin commands belong in `scripts`; tests belong in `tests`.
- Generated data belongs in `data/synthetic`, with its generator or provenance documented.
- Use deterministic seeds and UTC ISO-8601 timestamps where applicable.
- Never commit real financial or personally identifying data, secrets, or claims about a real institution.

## Metric convention

Define numerator and denominator, units, filters, and edge-case behavior. Percentiles use the nearest-rank method unless a chapter explicitly teaches another convention. Preserve raw observations so results are reproducible.
