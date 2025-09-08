import pandas as pd
import os
from pathlib import Path

def clean_fred_data(file_path, series_name):
    """
    Clean FRED economic data CSV files
    
    Parameters:
    file_path (str): Path to the CSV file
    series_name (str): Name for the value column
    
    Returns:
    pandas.DataFrame: Cleaned DataFrame with date and value columns
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        print(f"Successfully read {file_path}")
        print(f"Original shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # FRED data typically has two columns: DATE and the series value
        # Let's standardize the column names
        if len(df.columns) >= 2:
            # Rename columns to standard names
            df.columns = ['date', 'value']
            
            # Convert date to datetime
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Convert value to numeric, handling errors
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
            
            # Drop rows with missing values
            df = df.dropna()
            
            # Remove duplicates
            df = df.drop_duplicates(subset=['date'])
            
            # Rename value column to the series name
            df = df.rename(columns={'value': series_name})
            
            print(f"After cleaning shape: {df.shape}")
            return df
        else:
            print(f"Warning: File {file_path} has insufficient columns")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return pd.DataFrame()

def main():
    # Define paths
    base_dir = Path(__file__).parent.parent  # Go up one level from scripts folder
    raw_data_dir = base_dir / "data" / "raw"
    processed_data_dir = base_dir / "data" / "processed"
    
    # Create processed directory if it doesn't exist
    processed_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Define the datasets to process
    datasets = {
        "cpi": "CPIAUCSL",  # Consumer Price Index
        "fedfunds": "FEDFUNDS",  # Federal Funds Rate
        "gdp": "GDP",  # Gross Domestic Product
        "unemployment": "UNRATE"  # Unemployment Rate
    }
    
    # Process each dataset
    processed_dfs = {}
    
    for name, filename in datasets.items():
        file_path = raw_data_dir / f"{filename}.csv"
        print(f"\nProcessing {name} from {file_path}")
        
        if file_path.exists():
            # Clean the data
            df_clean = clean_fred_data(file_path, name)
            
            if not df_clean.empty:
                # Save cleaned data
                output_path = processed_data_dir / f"{name}_clean.csv"
                df_clean.to_csv(output_path, index=False)
                print(f"Saved cleaned data to {output_path}")
                
                # Store for merging
                processed_dfs[name] = df_clean
            else:
                print(f"No data remaining after cleaning for {name}")
        else:
            print(f"Raw data file not found: {file_path}")
    
    # Merge all datasets
    if processed_dfs:
        print("\nMerging datasets...")
        
        # Start with the first dataset
        merged_df = list(processed_dfs.values())[0]
        
        # Merge remaining datasets
        for name, df in list(processed_dfs.items())[1:]:
            merged_df = pd.merge(merged_df, df, on='date', how='outer')
        
        # Sort by date
        merged_df = merged_df.sort_values('date').reset_index(drop=True)
        
        # Save merged data
        merged_output_path = processed_data_dir / "merged_data.csv"
        merged_df.to_csv(merged_output_path, index=False)
        print(f"Merged data saved to {merged_output_path}")
        print(f"Merged data shape: {merged_df.shape}")
        print("\nFirst few rows of merged data:")
        print(merged_df.head())
    else:
        print("No data available to merge")

if __name__ == "__main__":
    main()