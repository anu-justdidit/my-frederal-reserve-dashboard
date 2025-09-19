# verify_dates.py
import pandas as pd
from datetime import datetime

print("✅ DATE VERIFICATION")
print("=" * 40)

# Test what date pandas creates
test_date = datetime(2025, 9, 20)
dates = pd.date_range(start='2000-01-01', end=test_date, freq='D')

print(f"Requested end date: {test_date.strftime('%Y-%m-%d')}")
print(f"Actual end date: {dates[-1].strftime('%Y-%m-%d')}")
print(f"Number of days: {len(dates)}")
print("=" * 40)

# Manual date creation
start_date = datetime(2000, 1, 1)
end_date = datetime(2025, 9, 20)
num_days = (end_date - start_date).days + 1
manual_dates = [start_date + pd.Timedelta(days=i) for i in range(num_days)]

print(f"Manual end date: {manual_dates[-1].strftime('%Y-%m-%d')}")
print(f"Manual days: {len(manual_dates)}")
print("=" * 40)