#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.backend_performance import add_transaction_index, benchmark_query, create_database, query_plan

db = create_database(); before_plan = query_plan(db); before = benchmark_query(db)
before_pages = db.execute("PRAGMA page_count").fetchone()[0]
add_transaction_index(db); after_plan = query_plan(db); after = benchmark_query(db)
after_pages = db.execute("PRAGMA page_count").fetchone()[0]
print("Harbor FCU Index Experiment")
print(f"BEFORE plan: {before_plan}")
print(f"AFTER plan:  {after_plan}")
print(f"Observed median: {before['median_ms']:.3f} -> {after['median_ms']:.3f} ms (machine-dependent)")
print(f"Database pages: {before_pages} -> {after_pages} (index storage tradeoff: +{after_pages-before_pages})")
print("Supported: this index changed this access plan under this synthetic workload.")
