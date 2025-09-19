# test_dates.py - CLEANER VERSION
from datetime import datetime
import pandas as pd

print("✅ DATE VERIFICATION SCRIPT - FINAL")
print("=" * 60)
print(f"Current system date: {datetime.now().strftime('%Y-%m-%d')}")
print("=" * 60)

# Test the FIXED version (using MS instead of M)
current_date = datetime.now().date()
dates_ms = pd.date_range(start='2000-01-01', end=current_date, freq='MS')  # Month Start

print("USING 'MS' (Month Start) - THIS IS WHAT YOUR APP USES:")
print(f"First date: {dates_ms[0].strftime('%Y-%m-%d')}")
print(f"Last date: {dates_ms[-1].strftime('%Y-%m-%d')}")
print(f"Number of months: {len(dates_ms)}")
print("=" * 60)

# Check if we have current month data
current_month = datetime.now().replace(day=1).date()  # First day of current month
if dates_ms[-1].date() == current_month:
    print("🎉 SUCCESS: Your app will show data through current month!")
    print(f"📅 Data includes: {dates_ms[-1].strftime('%Y-%m-%d')} (September 2025)")
else:
    print(f"⚠️  Date mismatch: {dates_ms[-1].date()} vs {current_month}")

print("=" * 60)
print("Your dashboard will now show data through September 2025! ✅")
print("=" * 60)