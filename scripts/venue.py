import os
import json
import pandas as pd
from utils.mappings import VENUE_MAPPING

DATA_FOLDER = "C:/Users/vishu/Downloads/ipl data pipeline/raw data"
files = os.listdir(DATA_FOLDER)
venues = set()
for filename in files:

    if filename.endswith(".json"):

        file_path = os.path.join(DATA_FOLDER, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            match_data = json.load(file)
            match_record = {}
        venue = match_data["info"]["venue"]
        venue = VENUE_MAPPING.get(venue, venue)
        venues.add(venue)

df = pd.DataFrame(
    sorted(venues),
    columns=["venue_name"])

print(len(venues))
print(df.head())
print(df.isnull().sum())

df.to_csv("../silver/dim_venues.csv", index=False)
df.to_parquet("../silver/dim_venues.parquet", index=False)
