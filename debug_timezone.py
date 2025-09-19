
# debug_timezone.py - Place this in your ROOT directory
from datetime import datetime, timezone
import pandas as pd

print("🕒 TIMEZONE DEBUG SCRIPT")
print("=" * 50)
print(f"Local time: {datetime.now()}")
print(f"UTC time: {datetime.now(timezone.utc)}")
print(f"Local date: {datetime.now().date()}")
print(f"UTC date: {datetime.now(timezone.utc).date()}")
print("=" * 50)

# Test date ranges with both timezone approaches
current_date_utc = datetime.now(timezone.utc).date()
current_date_local = datetime.now().date()

print("TESTING DATE RANGES:")
print("=" * 50)

# Test with UTC date
dates_utc = pd.date_range(start='2000-01-01', end=current_date_utc, freq='MS')
print(f"Using UTC date ({current_date_utc}):")
print(f"First date: {dates_utc[0].strftime('%Y-%m-%d')}")
print(f"Last date: {dates_utc[-1].strftime('%Y-%m-%d')}")
print(f"Number of months: {len(dates_utc)}")

print("-" * 30)

# Test with local date
dates_local = pd.date_range(start='2000-01-01', end=current_date_local, freq='MS')
print(f"Using local date ({current_date_local}):")
print(f"First date: {dates_local[0].strftime('%Y-%m-%d')}")
print(f"Last date: {dates_local[-1].strftime('%Y-%m-%d')}")
print(f"Number of months: {len(dates_local)}")

print("=" * 50)

# Check if dates are different
if dates_utc[-1] != dates_local[-1]:
    print("⚠️  WARNING: UTC and local dates give different results!")
    print(f"UTC result: {dates_utc[-1].strftime('%Y-%m-%d')}")
    print(f"Local result: {dates_local[-1].strftime('%Y-%m-%d')}")
else:
    print("✅ UTC and local dates give the same result")

print("=" * 50)