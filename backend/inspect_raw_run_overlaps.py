import pandas as pd

path = "../data/raw/realtime_manufacturing_dataset/state_events_100k.csv"
df = pd.read_csv(path)
df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
df["event_end"] = df["event_timestamp"] + pd.to_timedelta(
    df["duration_seconds"], unit="s"
)

runs = df[df["event_type"] == "RUN"].sort_values(
    ["machine_id", "event_timestamp"]
)

examples = []

for machine_id, group in runs.groupby("machine_id"):
    records = group.to_dict("records")

    for i, a in enumerate(records):
        for b in records[i + 1:]:
            if b["event_timestamp"] >= a["event_end"]:
                break

            if a["product_id"] != b["product_id"]:
                examples.append({
                    "machine_id": machine_id,
                    "event_a": a["event_id"],
                    "product_a": a["product_id"],
                    "start_a": a["event_timestamp"],
                    "duration_a": a["duration_seconds"],
                    "event_b": b["event_id"],
                    "product_b": b["product_id"],
                    "start_b": b["event_timestamp"],
                    "duration_b": b["duration_seconds"],
                })

print(pd.DataFrame(examples).head(15).to_string(index=False))
