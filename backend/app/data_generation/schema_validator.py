
from app.data_generation.data_loader import load_all_datasets


# Required columns for each manufacturing dataset
REQUIRED_COLUMNS = {
    "plants": [
        "plant_id",
    ],
    "lines": [
        "line_id",
        "plant",
    ],
    "machines": [
        "machine_id",
        "line_id",
    ],
    "products": [
        "product_id",
        "standard_cycle_time_sec",
    ],
    "shifts": [
        "shift_id",
    ],
    "production_orders": [
        "machine_id",
        "line_id",
        "product_id",
        "shift_id",
    ],
    "production_counts": [
        "machine_id",
        "product_id",
    ],
    "quality_inspections": [
        "machine_id",
        "product_id",
    ],
    "state_events": [
        "machine_id",
        "event_type",
    ],
}


def validate_schema(datasets):
    """
    Check whether each dataset contains its required columns.
    """

    validation_results = {}

    for dataset_name, required_columns in REQUIRED_COLUMNS.items():

        dataframe = datasets[dataset_name]

        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:

            validation_results[dataset_name] = {
                "status": "FAILED",
                "missing_columns": missing_columns,
            }

        else:

            validation_results[dataset_name] = {
                "status": "PASSED",
                "missing_columns": [],
            }

    return validation_results


if __name__ == "__main__":

    datasets = load_all_datasets()

    results = validate_schema(datasets)

    print("\nSCHEMA VALIDATION RESULTS")

    for dataset_name, result in results.items():

        print(
            f"{dataset_name}: {result['status']}"
        )

        if result["missing_columns"]:

            print(
                "Missing columns:",
                result["missing_columns"]
            )

    failed_count = sum(
        1
        for result in results.values()
        if result["status"] == "FAILED"
    )

    print("\nTotal datasets:", len(results))
    print("Failed datasets:", failed_count)
    print("Passed datasets:", len(results) - failed_count)
