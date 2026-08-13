#!/usr/bin/env python3
"""Chapter 33 interpretable incident-priority comparison."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.intelligence import compare_prioritizers, explain_priority, incident_scenario, score_priority

rows = incident_scenario(); results = compare_prioritizers(rows)
for title, key in (("RULE BASELINE", "rule"), ("SCORING MODEL", "scoring")):
    matrix = results[key]; print(f"{title}\nTP={matrix.true_positive} FP={matrix.false_positive} TN={matrix.true_negative} FN={matrix.false_negative}")
    print(f"Precision: {matrix.precision:.1%}\nRecall:    {matrix.recall:.1%}\n")
example = next(row for row in rows if score_priority(row))
print(f"WHY {example['id']} WAS PRIORITIZED")
for reason in explain_priority(example): print(f"- {reason}")
