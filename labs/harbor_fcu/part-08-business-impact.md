# Part VIII laboratory guide

Harbor Federal Credit Union and every observation are fictional and synthetic. Run Chapters 35–39 from the repository root:

```bash
python3 scripts/operational_scorecard.py
python3 scripts/measure_member_outcomes.py
python3 scripts/estimate_business_value.py
python3 scripts/report_outcomes.py --audience engineer
python3 scripts/report_outcomes.py --audience operations
python3 scripts/report_outcomes.py --audience executive
python3 scripts/run_capstone.py
```

These deterministic standard-library commands make no network calls. Values come from the shared executable outcome fixture. Estimates are assumption-dependent equivalents, never claims of realized savings.
