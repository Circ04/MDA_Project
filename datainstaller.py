import pandas as pd
import requests
import os

os.makedirs("data", exist_ok=True)

base_url = "https://opendata.apps.mow.vlaanderen.be/fietstellingen/"

# Download all monthly files
files = []
for year in range(2019, 2027):
    for month in range(1, 13):
        if year == 2019 and month < 8: continue
        if year == 2026 and month > 2: break
        files.append(f"data-{year}-{month:02d}.csv")

for f in files:
    path = f"data/{f}"
    if os.path.exists(path): continue
    print(f"Downloading {f}...")
    r = requests.get(base_url + f)
    if r.status_code == 200:
        open(path, "wb").write(r.content)

# Also grab metadata
for f in ["sites.csv", "richtingen.csv"]:
    path = f"data/{f}"
    if not os.path.exists(path):
        r = requests.get(base_url + f)
        if r.status_code == 200:
            open(path, "wb").write(r.content)

print("Done downloading. Now loading...")

# Concat everything
dfs = []
for f in sorted(os.listdir("data")):
    if f.startswith("data-") and f.endswith(".csv"):
        dfs.append(pd.read_csv(f"data/{f}", sep=";", low_memory=False))

df = pd.concat(dfs, ignore_index=True)
print(f"Total rows: {len(df):,}")
print(df.head())
print(df.dtypes)