import os
import json
import pandas as pd

# =====================================
# Configuration
# =====================================

DATA_FOLDER = r"C:\Users\vishu\Downloads\ipl data pipeline\raw data"

files = os.listdir(DATA_FOLDER)

TEAM_MAPPING = {
    "Kings XI Punjab": "Punjab Kings",
    "Delhi Daredevils": "Delhi Capitals",
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Rising Pune Supergiant": "Rising Pune Supergiants"
}

deliveries = []

# =====================================
# Read All Match Files
# =====================================

for filename in files:

    if not filename.endswith(".json"):
        continue

    file_path = os.path.join(DATA_FOLDER, filename)

    with open(file_path, "r", encoding="utf-8") as file:
        match_data = json.load(file)

    match_id = int(filename.replace(".json", ""))

    teams = match_data["info"]["teams"]

    team1 = TEAM_MAPPING.get(teams[0], teams[0])
    team2 = TEAM_MAPPING.get(teams[1], teams[1])

    # =====================================
    # Innings Loop
    # =====================================

    for innings_number, innings in enumerate(match_data["innings"], start=1):

        batting_team = TEAM_MAPPING.get(
            innings["team"],
            innings["team"]
        )

        if batting_team == team1:
            bowling_team = team2
        else:
            bowling_team = team1

        # =====================================
        # Over Loop
        # =====================================

        for over in innings["overs"]:

            over_number = over["over"]

            # =====================================
            # Delivery Loop
            # =====================================

            for delivery in over["deliveries"]:

                delivery_record = {}

                # Match Details
                delivery_record["match_id"] = match_id
                delivery_record["innings"] = innings_number
                delivery_record["batting_team"] = batting_team
                delivery_record["bowling_team"] = bowling_team

                # Ball Details
                delivery_record["over"] = over_number
                delivery_record["ball"] = delivery["actual_delivery"]

                # Players
                delivery_record["batter"] = delivery["batter"]
                delivery_record["bowler"] = delivery["bowler"]
                delivery_record["non_striker"] = delivery["non_striker"]

                # Runs
                batter_runs = delivery["runs"]["batter"]
                extras = delivery["runs"]["extras"]
                total_runs = delivery["runs"]["total"]

                delivery_record["batter_runs"] = batter_runs
                delivery_record["extras"] = extras
                delivery_record["total_runs"] = total_runs

                # Analytics Columns
                delivery_record["is_four"] = batter_runs == 4
                delivery_record["is_six"] = batter_runs == 6

                # Legal Delivery
                extras_info = delivery.get("extras", {})

                delivery_record["legal_delivery"] = (
                    "wides" not in extras_info
                )

                # Wickets
                if "wickets" in delivery:

                    wicket = delivery["wickets"][0]

                    delivery_record["is_wicket"] = True
                    delivery_record["player_out"] = wicket["player_out"]
                    delivery_record["dismissal_type"] = wicket["kind"]

                else:

                    delivery_record["is_wicket"] = False
                    delivery_record["player_out"] = None
                    delivery_record["dismissal_type"] = None

                deliveries.append(delivery_record)

# =====================================
# Create DataFrame
# =====================================

df = pd.DataFrame(deliveries)

print("=" * 70)
print("Total Deliveries :", len(df))
print("=" * 70)

print(df.head())

print("\nMissing Values\n")
print(df.isnull().sum())

print("\nColumns\n")
print(df.columns.tolist())

print("\nData Types\n")
print(df.dtypes)

print("\nInnings Distribution\n")
print(df["innings"].value_counts().sort_index())

# =====================================
# Save Silver Layer
# =====================================

os.makedirs("../silver", exist_ok=True)

df.to_csv(
    "../silver/fact_deliveries.csv",
    index=False
)

df.to_parquet(
    "../silver/fact_deliveries.parquet",
    index=False
)

print("\nFact Deliveries Created Successfully!")