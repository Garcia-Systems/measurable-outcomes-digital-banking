# Part VII laboratory guide

All observations are deterministic and synthetic. Run from the repository root with Python 3.10+; only the standard library is used.

```bash
python3 scripts/analyze_operations.py
python3 scripts/detect_anomalies.py
python3 scripts/forecast_workload.py
python3 scripts/prioritize_incidents.py
python3 scripts/run_intelligence_experiment.py
```

The sequence moves from grouping to detection, forecasting, explainable prioritization, and finally a controlled downstream workflow comparison. These are educational simulations, not production models. Re-run `python3 -m unittest discover -s tests -v` to verify ground truth and arithmetic.
