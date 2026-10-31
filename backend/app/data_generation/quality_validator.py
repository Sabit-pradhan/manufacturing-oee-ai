
from app.data_generation.data_loader import load_all_datasets


def check_missing_values(datasets):
    """Count missing values in every dataset."""

    results = {}

    for name, df in datasets.items():
        results[name] = int(df.isnull().sum().sum())

    return results


def check_duplicate_ids(datasets):
    """Check duplicate primary identifiers in master datasets."""

    id_columns = {
        "plants": "plant_id",
        "lines": "line_id",
        "machines": "machine_id",
        "products": "product_id",
    }

    results = {}

    for dataset_name, column in id_columns.items():
        df = datasets[dataset_name]

        results[dataset_name] = int(
            df[column].duplicated().sum()
        )

    return results


def check_invalid_references(datasets):
    """Check machine and product references."""

    valid_machine_ids = set(
        datasets["machines"]["machine_id"].dropna()
    )

    valid_product_ids = set(
        datasets["products"]["product_id"].dropna()
    )

    results = {}

    for dataset_name in [
        "production_orders",
        "production_counts",
        "quality_inspections",
        "state_events",
    ]:
        df = datasets[dataset_name]

        invalid_machines = (
            ~df["machine_id"].isin(valid_machine_ids)
        ).sum()

        invalid_products = (
            ~df["product_id"].isin(valid_product_ids)
        ).sum() if "product_id" in df.columns else 0

        results[dataset_name] = {
            "invalid_machine_references": int(invalid_machines),
            "invalid_product_references": int(invalid_products),
        }

    return results


def check_invalid_quantities(datasets):
    """Check negative quantities and impossible count relationships."""

    df = datasets["production_counts"]

    results = {
        "negative_total_count": int((df["total_count"] < 0).sum()),
        "negative_good_count": int((df["good_count"] < 0).sum()),
        "negative_reject_count": int((df["reject_count"] < 0).sum()),
        "good_plus_reject_exceeds_total": int(
            (
                df["good_count"] + df["reject_count"]
                > df["total_count"]
            ).sum()
        ),
    }

    return results


def check_event_severity(datasets):
    """
    Severity is required for FAULT and MICRO_STOP events.
    It is optional for other event types in this source dataset.
    """

    df = datasets["state_events"]

    required_events = ["FAULT", "MICRO_STOP"]

    required_records = df[
        df["event_type"].isin(required_events)
    ]

    missing_required_severity = int(
        required_records["severity"].isna().sum()
    )

    optional_records = df[
        ~df["event_type"].isin(required_events)
    ]

    expected_missing_severity = int(
        optional_records["severity"].isna().sum()
    )

    return {
        "missing_severity_in_required_events":
            missing_required_severity,
        "expected_missing_severity":
            expected_missing_severity,
    }


if __name__ == "__main__":

    datasets = load_all_datasets()

    print("\nMISSING VALUE CHECK")
    print(check_missing_values(datasets))

    print("\nDUPLICATE ID CHECK")
    print(check_duplicate_ids(datasets))

    print("\nINVALID REFERENCE CHECK")
    print(check_invalid_references(datasets))

    print("\nINVALID QUANTITY CHECK")
    print(check_invalid_quantities(datasets))

    print("\nEVENT SEVERITY CHECK")
    print(check_event_severity(datasets))
