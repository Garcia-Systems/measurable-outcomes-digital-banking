# Part VI laboratory guide

All Harbor FCU data, candidates, defects, users, transfers, and security values are fictional and synthetic. Run from the repository root with Python 3.10+:

```bash
python3 scripts/measure_testing.py
python3 scripts/analyze_defect_escape.py
python3 scripts/run_security_validation.py
python3 scripts/check_release_readiness.py
python3 scripts/check_release_readiness.py --candidate invalid
python3 scripts/run_delivery_experiment.py
```

Commands are deterministic and network-free. The invalid candidate's `DEPLOYMENT READY NO` is an expected observation. Passing defined fixtures does not establish universal security or production infallibility.
