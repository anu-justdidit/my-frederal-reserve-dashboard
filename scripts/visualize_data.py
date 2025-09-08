import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/merged_data.csv", parse_dates=["Date"], index_col="Date")

# Plot each column
for col in df.columns:
    df[col].plot(title=col)
    plt.show()
