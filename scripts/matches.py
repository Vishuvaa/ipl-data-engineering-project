import os
import json
import pandas as pd
import pyarrow
from utils.mappings import TEAM_MAPPING, VENUE_MAPPING

DATA_FOLDER = "C:/Users/vishu/Downloads/ipl data pipeline/raw data"

files = os.listdir(DATA_FOLDER)

venues = set()
matches = []
for filename in files:

    if filename.endswith(".json"):

        file_path = os.path.join(DATA_FOLDER, filename)

        with open(file_path, "r", encoding="utf-8") as file:
            match_data = json.load(file)
            match_record = {}
            match_record["match_id"] = int(filename.replace(".json", ""))
            match_date = match_data["info"]["dates"][0]
            match_record["year"] = int(match_date[:4])
            match_record["match_date"] = match_date
            match_record["city"] = match_data["info"].get("city", "Unknown")
            venue = match_data["info"]["venue"]
            match_record["venue"] = VENUE_MAPPING.get(venue, venue)
            match_record["team1"] = TEAM_MAPPING.get(match_data["info"]["teams"][0], match_data["info"]["teams"][0])

            match_record["team2"] = TEAM_MAPPING.get(match_data["info"]["teams"][1], match_data["info"]["teams"][1])

            winner = match_data["info"]["outcome"].get("winner")
            match_record["winner"] = TEAM_MAPPING.get(winner, winner)

            toss_winner = match_data["info"]["toss"]["winner"]
            match_record["toss_winner"] = TEAM_MAPPING.get(toss_winner, toss_winner)
            match_record["toss_decision"] = match_data["info"]["toss"]["decision"]
            match_data["info"]["outcome"].get("winner")
            player = match_data["info"].get("player_of_match", [])
            match_record["player_of_the_match"] = player[0] if player else None
            matches.append(match_record)
print(f"Total Matches Extracted: {len(matches)}")
print(matches[0])
print(matches[-1])

df = pd.DataFrame(matches)
print(df.head())
print(df.isnull().sum())

df.to_csv("../silver/dim_matches.csv", index=False)
df.to_parquet("../silver/dim_matches.parquet", index=False)


