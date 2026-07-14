import os
import json
import pandas as pd

DATA_FOLDER = "C:/Users/vishu/Downloads/ipl data pipeline/raw data"

files = os.listdir(DATA_FOLDER)

TEAM_MAPPING = {
    "Kings XI Punjab": "Punjab Kings",
    "Delhi Daredevils": "Delhi Capitals",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiant": "Rising Pune Supergiants"
}

teams = set()
for filename in files:

    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(DATA_FOLDER, filename)

    with open(file_path, "r", encoding="utf-8") as file:

        match_data = json.load(file)

        for team in match_data["info"]["teams"]:

            # Standardize Team Name
            team = TEAM_MAPPING.get(team, team)

            teams.add(team)

df = pd.DataFrame(
    sorted(teams),
    columns=["team_name"]
)

print(df)

print(f"\nTotal Unique Teams : {len(df)}")

os.makedirs("../silver", exist_ok=True)

df.to_csv("../silver/dim_teams.csv", index=False)

df.to_parquet("../silver/dim_teams.parquet", index=False)

print("\nTeams Dimension Created Successfully!")