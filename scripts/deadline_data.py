import subprocess

def run_pipeline():
    print(" Running pipeline...")
    subprocess.run(["python", "scripts/download_data.py"])
    subprocess.run(["python", "scripts/clean_data.py"])
    print("✅ Pipeline complete!")

if __name__ == "__main__":
    run_pipeline()
