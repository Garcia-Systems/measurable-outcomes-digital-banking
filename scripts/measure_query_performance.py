#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.backend_performance import benchmark_query, create_database, query_plan

result = benchmark_query(create_database())
print("Harbor FCU Recent Transactions Query (synthetic)")
print(f"Executions: {result['executions']}")
print(f"Median: {result['median_ms']:.3f} ms")
print(f"p95: {result['p95_ms']:.3f} ms")
print(f"Maximum: {result['maximum_ms']:.3f} ms")
print(f"Rows returned: {result['rows_returned']}")
print(f"Query plan: {query_plan(create_database())}")
print("Wall-clock values are machine-dependent; result count and plan are structural evidence.")
