import os
import json
import pandas as pd

DATA_FOLDER = "C:/Users/vishu/Downloads/ipl data pipeline/raw data"
files = os.listdir(DATA_FOLDER)

players = {}
for filename in files:
    if not filename.endswith(".json"):
        continue
    file_path = os.path.join(DATA_FOLDER, filename)
    with open(file_path, "r", encoding="utf-8") as file:
        match_data = json.load(file)
        registry = match_data["info"]["registry"]["people"]
        teams = match_data["info"]["players"]
        # Loop through both teams
        for team in teams.values():
            # Loop through every player
            for player_name in team:
                # Get player's unique ID
                player_id = registry[player_name]
                # Store in dictionary
                players[player_id] = player_name

df = pd.DataFrame(
    players.items(),
    columns=["player_id", "player_name"]
)

df = df.sort_values("player_name").reset_index(drop=True)

print(df)

print(f"\nTotal Unique Players : {len(df)}")

os.makedirs("../silver", exist_ok=True)
df.to_csv("../silver/dim_players.csv", index=False)
df.to_parquet("../silver/dim_players.parquet", index=False)