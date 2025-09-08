"""
download_data.py
Fetches economic data from FRED and saves as CSV.
Author: Anusha
"""

import os
import sys
import logging
import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv

# -----------------------------
# Load .env from project root
# -----------------------------
# This ensures Python finds your .env even if you run from scripts/
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

API_KEY = os.getenv("FRED_API_KEY")
if not API_KEY:
    logging.error("❌ FRED_API_KEY not found. Make sure it's in your .env file!")
    sys.exit(1)

# -----------------------------
# Setup logging
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

fred = Fred(api_key=API_KEY)
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

# -----------------------------
# Functions
# -----------------------------
def download_series(series_id: str, start="2000-01-01") -> pd.DataFrame:
    try:
        logging.info(f"⬇️ Downloading {series_id}")
        data = fred.get_series(series_id, observation_start=start)
        df = pd.DataFrame(data).reset_index()
        df.columns = ["date", series_id]
        return df
    except Exception as e:
        logging.error(f"⚠️ Failed to download {series_id}: {e}")
        return pd.DataFrame()

def save_to_csv(df: pd.DataFrame, filename: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(filepath, index=False)
    logging.info(f"💾 Saved: {filepath}")

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    logging.info("🚀 Starting FRED data download...")

    series_list = {
        "GDP": "GDP.csv",
        "CPIAUCSL": "CPI.csv",
        "UNRATE": "Unemployment.csv",
        "FEDFUNDS": "FedFunds.csv"
    }

    for series_id, filename in series_list.items():
        df = download_series(series_id)
        if not df.empty:
            save_to_csv(df, filename)

    logging.info("✅ All downloads complete!")
