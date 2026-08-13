#!/usr/bin/env python3
CLAIMS=[
 ("Application completion increased in the controlled measurement.","observation"),
 ("More measured sessions successfully completed the workflow.","interpretation"),
 ("The change may reduce demand for assistance.","hypothesis"),
 ("The change saved Harbor FCU $100,000.","unsupported causal claim"),
]
print("Harbor FCU Evidence-Strength Exercise (answer key)")
for statement,classification in CLAIMS: print(f"- {classification.upper()}: {statement}")
print("Only measured observations and bounded interpretations are supported; downstream effects need evidence.")
