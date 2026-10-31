import pandas as pd
from pathlib import Path

data_dir = Path("../data/processed")

files = [
    "count_corrections.csv",
    "production_counts.csv",
    "quality_inspections.csv",
    "state_events.csv",
    "ideal_cycle_times.csv",
]

for filename in files:
    df = pd.read_csv(data_dir / filename, nrows=3)

    print(f"\n--- {filename} ---")
    print("Columns:", df.columns.tolist())
    print(df.head(3).to_string(index=False))
