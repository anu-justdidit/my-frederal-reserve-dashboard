#!/usr/bin/env python3
"""
inspect_data.py - Quick data inspection
"""

import pandas as pd
from pathlib import Path

def main():
    print("🔍 Data Inspector")
    print("=" * 50)
    
    # Check if processed data exists
    processed_file = Path("data/processed/merged_data.csv")
    if processed_file.exists():
        df = pd.read_csv(processed_file)
        print(f"📁 Processed data: {df.shape}")
        print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
        print(f"📊 Columns: {list(df.columns)}")
    else:
        print("❌ No processed data found")
    
    # Check environment
    import os
    api_key = os.getenv("FRED_API_KEY")
    print(f"🔑 FRED API Key: {'✅ Set' if api_key else '❌ Missing'}")

if __name__ == "__main__":
    main()