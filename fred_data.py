
import os
import pandas as pd
import matplotlib.pyplot as plt
from fredapi import Fred

# Get your API key from environment variable
api_key = os.getenv("FRED_API_KEY")

if not api_key:
    raise ValueError("FRED_API_KEY not found. Please set it as an environment variable.")

# Initialize FRED
fred = Fred(api_key=api_key)

# Example: Fetch US GDP and Unemployment Rate
try:
    gdp = fred.get_series("GDP")
    unemployment = fred.get_series("UNRATE")
except Exception as e:
    raise RuntimeError(f"Error fetching data: {e}")

# Put into DataFrame
df = pd.DataFrame({
    "GDP": gdp,
    "Unemployment": unemployment
})

# Drop missing values
df = df.dropna()

# Show latest data
print("\nLatest Data:")
print(df.tail())

# Plot
df.plot(secondary_y="Unemployment", title="US GDP vs Unemployment")
plt.show()
