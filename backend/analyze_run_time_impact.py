import pandas as pd

df = pd.read_csv("../data/raw/realtime_manufacturing_dataset/state_events_100k.csv")
df = df[df["event_type"] == "RUN"].copy()

df["start"] = pd.to_datetime(df["event_timestamp"])
df["end"] = df["start"] + pd.to_timedelta(df["duration_seconds"], unit="s")

def analyze(group):
    intervals = sorted(zip(group["start"], group["end"]))
    merged = []
    overlap_seconds = 0

    for start, end in intervals:
        if not merged or start >= merged[-1][1]:
            merged.append([start, end])
        else:
            overlap_seconds += (min(end, merged[-1][1]) - start).total_seconds()
            merged[-1][1] = max(merged[-1][1], end)

    union_seconds = sum((end - start).total_seconds() for start, end in merged)
    recorded_seconds = group["duration_seconds"].sum()

    return pd.Series({
        "run_events": len(group),
        "recorded_run_hours": recorded_seconds / 3600,
        "unique_run_hours": union_seconds / 3600,
        "overlap_excess_hours": (recorded_seconds - union_seconds) / 3600,
    })

result = df.groupby("machine_id").apply(analyze)
print(result.round(2).to_string())
print("\nTOTALS:")
print(result.sum().round(2))
