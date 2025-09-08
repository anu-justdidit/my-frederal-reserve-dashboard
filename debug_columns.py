
# debug_columns.py
import pandas as pd
from pathlib import Path

def check_columns():
    try:
        # Path to your merged data
        file_path = Path("data/processed/merged_data.csv")
        
        print("=" * 50)
        print("DEBUGGING YOUR MERGED DATA FILE")
        print("=" * 50)
        
        print(f"📁 Checking file: {file_path}")
        print(f"✅ File exists: {file_path.exists()}")
        
        if file_path.exists():
            # Read the data
            df = pd.read_csv(file_path)
            
            print(f"\n📊 Shape: {df.shape} (rows, columns)")
            print(f"🏷️ Columns: {list(df.columns)}")
            
            print(f"\n👀 First 3 rows:")
            print(df.head(3))
            
            print(f"\n📋 Column details:")
            for i, col in enumerate(df.columns):
                sample_value = df[col].iloc[0] if len(df) > 0 else "N/A"
                print(f"   {i+1}. '{col}' -> {df[col].dtype}, sample: {sample_value}")
                
            print(f"\n💡 This shows why your dashboard failed!")
            print(f"💡 Your columns are: {list(df.columns)}")
            print(f"💡 But dashboard expected a column named 'date'")
            
        else:
            print(f"\n❌ ERROR: File not found!")
            print(f"❌ Please run: python scripts/clean_data.py")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    check_columns()
    print(f"\n🎯 Now share this output to fix the dashboard!")