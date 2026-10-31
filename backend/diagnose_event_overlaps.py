
import csv
from pathlib import Path

from sqlalchemy import text
from app.database.connection import engine


OVERLAP_SUMMARY_QUERY = text("""
    WITH overlapping_events AS (
        SELECT
            a.event_id AS event_a,
            b.event_id AS event_b,
            a.machine_id,

            LEAST(a.event_type, b.event_type) AS event_type_a,
            GREATEST(a.event_type, b.event_type) AS event_type_b,

            GREATEST(
                a.event_timestamp,
                b.event_timestamp
            ) AS overlap_start,

            LEAST(
                a.event_timestamp
                    + (a.duration_seconds * INTERVAL '1 second'),
                b.event_timestamp
                    + (b.duration_seconds * INTERVAL '1 second')
            ) AS overlap_end

        FROM state_events a
        JOIN state_events b
          ON a.machine_id = b.machine_id
         AND a.event_id < b.event_id

         AND a.event_timestamp <
             b.event_timestamp
             + (COALESCE(b.duration_seconds, 0) * INTERVAL '1 second')

         AND b.event_timestamp <
             a.event_timestamp
             + (COALESCE(a.duration_seconds, 0) * INTERVAL '1 second')

        WHERE COALESCE(a.duration_seconds, 0) > 0
          AND COALESCE(b.duration_seconds, 0) > 0
    ),

    overlap_durations AS (
        SELECT
            event_a,
            event_b,
            machine_id,
            event_type_a,
            event_type_b,

            EXTRACT(
                EPOCH FROM (overlap_end - overlap_start)
            ) AS overlap_seconds

        FROM overlapping_events
    )

    SELECT
        event_type_a,
        event_type_b,

        COUNT(*) AS overlapping_pairs,

        COUNT(DISTINCT machine_id) AS affected_machines,

        ROUND(SUM(overlap_seconds)::numeric, 2)
            AS total_pairwise_overlap_sec,

        ROUND(
            (SUM(overlap_seconds) / 3600)::numeric,
            2
        ) AS total_pairwise_overlap_hours,

        ROUND(AVG(overlap_seconds)::numeric, 2)
            AS average_overlap_sec,

        ROUND(MAX(overlap_seconds)::numeric, 2)
            AS maximum_overlap_sec

    FROM overlap_durations

    GROUP BY event_type_a, event_type_b

    ORDER BY overlapping_pairs DESC
""")


TOTAL_QUERY = text("""
    SELECT
        COUNT(*) AS overlapping_pairs,
        COUNT(DISTINCT a.machine_id) AS affected_machines
    FROM state_events a
    JOIN state_events b
      ON a.machine_id = b.machine_id
     AND a.event_id < b.event_id

     AND a.event_timestamp <
         b.event_timestamp
         + (COALESCE(b.duration_seconds, 0) * INTERVAL '1 second')

     AND b.event_timestamp <
         a.event_timestamp
         + (COALESCE(a.duration_seconds, 0) * INTERVAL '1 second')

    WHERE COALESCE(a.duration_seconds, 0) > 0
      AND COALESCE(b.duration_seconds, 0) > 0
""")


def main():
    with engine.connect() as connection:

        print("\n1. OVERLAP SUMMARY BY EVENT TYPE")

        rows = connection.execute(
            OVERLAP_SUMMARY_QUERY
        ).mappings().all()

        if not rows:
            print("No overlapping events found.")
            return

        headers = list(rows[0].keys())

        for row in rows:
            print(dict(row))

        print("\n2. OVERALL SUMMARY")

        total = connection.execute(
            TOTAL_QUERY
        ).mappings().first()

        print(dict(total))

        # Export the grouped summary to CSV.
        output_file = (
            Path(__file__).resolve().parent
            / "event_overlap_summary.csv"
        )

        with output_file.open(
            "w",
            newline="",
            encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=headers
            )

            writer.writeheader()
            writer.writerows(
                [dict(row) for row in rows]
            )

        print("\n3. CSV REPORT")

        print(f"Saved to: {output_file}")

        print("\nOverlap diagnostic completed.")


if __name__ == "__main__":
    main()
