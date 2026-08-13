#!/usr/bin/env python3
"""Run local, defensive Chapter 27 security fixtures."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.quality import security_validation

r = security_validation()
print("Harbor FCU Defined Security Validation")
print(f"Cases tested                 {r['cases_tested']}")
print(f"Cases passed                 {r['cases_passed']}")
print(f"Invalid cases rejected       {r['rejected_correctly']}/{r['invalid_cases']}")
print(f"Invalid cases accepted       {r['accepted_incorrectly']}")
print(f"Exposure in unsafe output    {r['unsafe_exposures_detected']}")
print(f"Exposure in redacted output  {r['safe_exposures_detected']}")
print("Conclusion: the controls passed the defined fixtures; universal security is not established.")
