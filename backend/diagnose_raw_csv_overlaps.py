import pandas as pd

path = "../data/raw/realtime_manufacturing_dataset/state_events_100k.csv"
df = pd.read_csv(path)

df["event_timestamp"] = pd.to_datetime(df["event_timestamp"])
df["event_end"] = df["event_timestamp"] + pd.to_timedelta(
    df["duration_seconds"], unit="s"
)

df = df.sort_values(["machine_id", "event_timestamp"])

total_pairs = 0
run_pairs = 0
different_product_pairs = 0
same_product_pairs = 0

for machine_id, group in df.groupby("machine_id"):
    records = group.to_dict("records")

    for i, a in enumerate(records):
        for b in records[i + 1:]:
            if b["event_timestamp"] >= a["event_end"]:
                break

            if a["event_timestamp"] < b["event_end"]:
                total_pairs += 1

                if a["event_type"] == "RUN" and b["event_type"] == "RUN":
                    run_pairs += 1

                    if a["product_id"] == b["product_id"]:
                        same_product_pairs += 1
                    else:
                        different_product_pairs += 1

print("RAW CSV OVERLAP RESULTS")
print("Total overlapping pairs:", total_pairs)
print("RUN + RUN pairs:", run_pairs)
print("RUN + RUN, same product:", same_product_pairs)
print("RUN + RUN, different product:", different_product_pairs)
