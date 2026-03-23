import pandas as pd
import os

data_dir = "data"
dfs = []
col_names = ["site_id", "richting", "type", "van", "tot", "aantal"]

csv_files = sorted([f for f in os.listdir(data_dir) if f.startswith("data-") and f.endswith(".csv")])

for f in csv_files:
    print(f"Processing {f}...")
    df = pd.read_csv(f"{data_dir}/{f}", header=None, names=col_names, low_memory=False)
    df = df[df["type"].str.upper().str.strip() == "FIETSERS"]
    dfs.append(df)
    print(f"  Kept {len(df):,} cyclist rows")

full = pd.concat(dfs, ignore_index=True)
print(f"\nTotal cyclist rows: {len(full):,}")

full.to_parquet(f"{data_dir}/cyclists_all.parquet", index=False)
print(f"Saved to {data_dir}/cyclists_all.parquet")