#!/usr/bin/env python3
import argparse, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.outcomes import audience_report

p = argparse.ArgumentParser(); p.add_argument("--audience", required=True, choices=("engineer", "operations", "executive"))
print(audience_report(p.parse_args().audience))
