
from pathlib import Path
import pandas as pd

from app.data_generation.data_loader import load_all_datasets
from app.data_generation.schema_validator import validate_schema
from app.data_generation.quality_validator import (
    check_missing_values,
    check_duplicate_ids,
    check_invalid_references,
    check_invalid_quantities,
    check_event_severity,
)


# Find the project root and report destination
PROJECT_ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = PROJECT_ROOT / "data" / "exports"

REPORT_FILE = REPORT_DIR / "data_validation_report.csv"


def generate_validation_report():
    """
    Run all validation checks and generate a consolidated CSV report.
    """

    print("\nLoading manufacturing datasets...")

    datasets = load_all_datasets()

    print("\nRunning validation checks...")

    schema_results = validate_schema(datasets)
    missing_results = check_missing_values(datasets)
    duplicate_results = check_duplicate_ids(datasets)
    reference_results = check_invalid_references(datasets)
    quantity_results = check_invalid_quantities(datasets)
    severity_results = check_event_severity(datasets)

    report_rows = []

    for dataset_name, df in datasets.items():

        schema_status = schema_results[dataset_name]["status"]

        missing_count = missing_results[dataset_name]

        duplicate_count = duplicate_results.get(
            dataset_name, 0
        )

        invalid_machine = reference_results.get(
            dataset_name, {}
        ).get("invalid_machine_references", 0)

        invalid_product = reference_results.get(
            dataset_name, {}
        ).get("invalid_product_references", 0)

        # Severity missing from non-FAULT and non-MICRO_STOP
        # events is expected according to our inspected source data.
        expected_missing = (
            severity_results["expected_missing_severity"]
            if dataset_name == "state_events"
            else 0
        )

        unexpected_missing = missing_count - expected_missing

        # Quantity checks apply to production_counts.
        quantity_violations = (
            sum(quantity_results.values())
            if dataset_name == "production_counts"
            else 0
        )

        # Missing required severity is a separate quality rule.
        required_severity_missing = (
            severity_results[
                "missing_severity_in_required_events"
            ]
            if dataset_name == "state_events"
            else 0
        )

        failed_checks = (
            schema_status == "FAILED"
            or unexpected_missing > 0
            or duplicate_count > 0
            or invalid_machine > 0
            or invalid_product > 0
            or quantity_violations > 0
            or required_severity_missing > 0
        )

        report_rows.append({
            "dataset": dataset_name,
            "total_records": len(df),
            "total_columns": len(df.columns),
            "schema_status": schema_status,
            "missing_values_total": missing_count,
            "expected_missing_values": expected_missing,
            "unexpected_missing_values": unexpected_missing,
            "duplicate_primary_ids": duplicate_count,
            "invalid_machine_references": invalid_machine,
            "invalid_product_references": invalid_product,
            "quantity_violations": quantity_violations,
            "missing_required_severity": required_severity_missing,
            "overall_status": (
                "FAILED" if failed_checks else "PASSED"
            ),
        })

    report_df = pd.DataFrame(report_rows)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report_df.to_csv(REPORT_FILE, index=False)

    print("\nDATA VALIDATION REPORT")
    print(report_df.to_string(index=False))

    print("\nREPORT SUMMARY")
    print("Total datasets:", len(report_df))
    print(
        "Passed datasets:",
        (report_df["overall_status"] == "PASSED").sum()
    )
    print(
        "Failed datasets:",
        (report_df["overall_status"] == "FAILED").sum()
    )

    print("\nReport saved successfully:")
    print(REPORT_FILE)


if __name__ == "__main__":
    generate_validation_report()
