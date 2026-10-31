
from pathlib import Path
import pandas as pd


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Directory containing processed CSV files
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"


# CSV files required for the initial validation pipeline
REQUIRED_DATASETS = {
    "plants": "plants.csv",
    "lines": "lines.csv",
    "machines": "machines.csv",
    "products": "products.csv",
    "shifts": "shifts.csv",
    "production_orders": "production_orders.csv",
    "production_counts": "production_counts.csv",
    "quality_inspections": "quality_inspections.csv",
    "state_events": "state_events.csv",
}


def load_csv(file_name: str) -> pd.DataFrame:
    """
    Load a CSV file and return it as a Pandas DataFrame.
    """

    file_path = PROCESSED_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


def load_all_datasets() -> dict[str, pd.DataFrame]:
    """
    Load all required manufacturing datasets.
    """

    datasets = {}

    for dataset_name, file_name in REQUIRED_DATASETS.items():

        print(f"Loading {dataset_name}...")

        datasets[dataset_name] = load_csv(file_name)

        print(
            f"Loaded {dataset_name}: "
            f"{len(datasets[dataset_name])} records"
        )

    return datasets


if __name__ == "__main__":

    data = load_all_datasets()

    print("\nDataset loading completed successfully.")

    print("\nDataset summary:")

    for name, dataframe in data.items():

        print(
            f"{name}: "
            f"{dataframe.shape[0]} rows, "
            f"{dataframe.shape[1]} columns"
        )
