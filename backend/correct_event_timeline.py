import pandas as pd
from pathlib import Path

SOURCE = Path("../data/raw/realtime_manufacturing_dataset/state_events_100k.csv")
OUTPUT = Path("../data/processed")
OUTPUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(SOURCE)
df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
df["duration_seconds"] = pd.to_numeric(df["duration_seconds"], errors="raise")

df["event_end"] = (
    df["event_timestamp"]
    + pd.to_timedelta(df["duration_seconds"], unit="s")
)

corrected = []
audit = []

for machine_id, group in df.groupby("machine_id"):
    runs = group[group["event_type"] == "RUN"].sort_values(
        ["event_timestamp", "event_id"]
    )

    occupied = []

    for event in runs.itertuples(index=False):
        start = event.event_timestamp
        end = event.event_end

        if end <= start:
            continue

        # Subtract only time already allocated to earlier RUN events.
        available = []
        cursor = start

        for occupied_start, occupied_end in occupied:
            if occupied_end <= cursor:
                continue
            if occupied_start >= end:
                break

            if cursor < occupied_start:
                available.append((cursor, min(occupied_start, end)))

            cursor = max(cursor, occupied_end)

            if cursor >= end:
                break

        if cursor < end:
            available.append((cursor, end))

        retained_seconds = 0

        for segment_number, (segment_start, segment_end) in enumerate(available, 1):
            seconds = int((segment_end - segment_start).total_seconds())

            if seconds <= 0:
                continue

            retained_seconds += seconds

            corrected.append({
                "event_id": f"{event.event_id}-R{segment_number:03d}",
                "source_event_id": event.event_id,
                "machine_id": event.machine_id,
                "line_id": event.line_id,
                "event_type": "RUN",
                "product_id": event.product_id,
                "event_timestamp": segment_start,
                "duration_seconds": seconds,
                "recorded_by": event.recorded_by,
                "severity": event.severity,
            })

            occupied.append((segment_start, segment_end))
            occupied.sort(key=lambda x: x[0])

        original_seconds = int(event.duration_seconds)
        removed_seconds = original_seconds - retained_seconds

        if removed_seconds > 0:
            audit.append({
                "source_event_id": event.event_id,
                "machine_id": machine_id,
                "product_id": event.product_id,
                "original_duration_seconds": original_seconds,
                "retained_duration_seconds": retained_seconds,
                "removed_overlap_seconds": removed_seconds,
            })

# Preserve every non-RUN event unchanged.
for event in df[df["event_type"] != "RUN"].itertuples(index=False):
    corrected.append({
        "event_id": event.event_id,
        "source_event_id": event.event_id,
        "machine_id": event.machine_id,
        "line_id": event.line_id,
        "event_type": event.event_type,
        "product_id": event.product_id,
        "event_timestamp": event.event_timestamp,
        "duration_seconds": int(event.duration_seconds),
        "recorded_by": event.recorded_by,
        "severity": event.severity,
    })

canonical = pd.DataFrame(corrected).sort_values(
    ["machine_id", "event_timestamp", "event_id"]
)

audit_df = pd.DataFrame(audit)

canonical.to_csv(OUTPUT / "state_events_canonical.csv", index=False)
audit_df.to_csv(OUTPUT / "state_event_conflicts.csv", index=False)

run_hours = canonical.loc[
    canonical["event_type"] == "RUN", "duration_seconds"
].sum() / 3600

removed_hours = audit_df["removed_overlap_seconds"].sum() / 3600

print("RUN TIMELINE CORRECTION COMPLETE")
print("Original event rows:", len(df))
print("Canonical event rows:", len(canonical))
print("RUN events before:", (df["event_type"] == "RUN").sum())
print("Canonical RUN segments:", (canonical["event_type"] == "RUN").sum())
print("RUN hours after correction:", round(run_hours, 2))
print("Removed overlapping RUN hours:", round(removed_hours, 2))
print("Non-RUN events preserved:", (canonical["event_type"] != "RUN").sum())
print("Duplicate canonical event IDs:", canonical["event_id"].duplicated().sum())
print("Canonical file:", OUTPUT / "state_events_canonical.csv")
print("Conflict audit:", OUTPUT / "state_event_conflicts.csv")
