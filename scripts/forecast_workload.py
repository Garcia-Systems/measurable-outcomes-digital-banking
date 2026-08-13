#!/usr/bin/env python3
"""Chapter 32 capacity forecasting laboratory."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from harbor_fcu.intelligence import forecast_error, forecast_recent_average, forecast_trend, workload_scenario

history, actual = workload_scenario(); recent = forecast_recent_average(history, len(actual)); trend = forecast_trend(history, len(actual))
print("Harbor FCU Digital Requests per Hour Forecast")
for name, predicted in (("RECENT AVERAGE", recent), ("TREND", trend)):
    error = forecast_error(actual, predicted)
    print(f"{name:14} forecast={[round(v, 1) for v in predicted]} MAE={error['mae']:.1f} RMSE={error['rmse']:.1f}")
print("An accurate synthetic forecast does not establish capacity cost savings.")
