import os
import pandas as pd

# =====================================
# Read Silver Layer
# =====================================

df = pd.read_parquet(
    r"C:\Users\vishu\Downloads\ipl data pipeline\silver\fact_deliveries.parquet"
)

# =====================================
# Group By Batter
# =====================================

grouped = df.groupby("batter")

# =====================================
# Total Runs
# =====================================

runs = (
    grouped["batter_runs"]
    .sum()
    .reset_index()
    .rename(columns={"batter_runs": "total_runs"})
)

# =====================================
# Innings Batted
# =====================================

innings = (
    df[["batter", "match_id", "innings"]]
    .drop_duplicates(subset=["batter", "match_id", "innings"])
    .groupby("batter")
    .size()
    .reset_index(name="innings")
)

# =====================================
# Balls Faced
# =====================================

legal_df = df[df["legal_delivery"]]

balls = (
    legal_df.groupby("batter")["legal_delivery"]
    .count()
    .reset_index()
    .rename(columns={"legal_delivery": "balls_faced"})
)

# =====================================
# Fours
# =====================================

fours = (
    grouped["is_four"]
    .sum()
    .reset_index()
    .rename(columns={"is_four": "fours"})
)

# =====================================
# Sixes
# =====================================

sixes = (
    grouped["is_six"]
    .sum()
    .reset_index()
    .rename(columns={"is_six": "sixes"})
)

# =====================================
# Merge All Statistics
# =====================================

player_stats = (
    runs
    .merge(innings, on="batter")
    .merge(balls, on="batter")
    .merge(fours, on="batter")
    .merge(sixes, on="batter")
)

# =====================================
# Strike Rate
# =====================================

player_stats["strike_rate"] = (
    player_stats["total_runs"] /
    player_stats["balls_faced"]
) * 100

player_stats["strike_rate"] = player_stats["strike_rate"].round(2)

# =====================================
# Arrange Columns
# =====================================

player_stats = player_stats[
    [
        "batter",
        "innings",
        "total_runs",
        "balls_faced",
        "fours",
        "sixes",
        "strike_rate"
    ]
]

# =====================================
# Sort by Runs
# =====================================

player_stats = player_stats.sort_values(
    by="total_runs",
    ascending=False
).reset_index(drop=True)

# =====================================
# Create Gold Folder
# =====================================

os.makedirs(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold",
    exist_ok=True
)

# =====================================
# Save Files
# =====================================

player_stats.to_csv(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold\player_statistics.csv",
    index=False
)

player_stats.to_parquet(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold\player_statistics.parquet",
    index=False
)

# =====================================
# Display Result
# =====================================

print("=" * 80)
print(player_stats.head(20))
print("=" * 80)

print(f"\nTotal Players : {len(player_stats)}")

print("\nGold Layer - Player Statistics Created Successfully!")

print(pd.read_parquet("C:/Users/vishu/Downloads/ipl data pipeline/silver/fact_deliveries.parquet").columns.tolist())
print(pd.read_parquet("C:/Users/vishu/Downloads/ipl data pipeline/silver/dim_matches.parquet").columns.tolist())
df = pd.read_parquet("C:/Users/vishu/Downloads/ipl data pipeline/silver/dim_players.parquet")
print(df.columns.tolist())
df = pd.read_parquet("C:/Users/vishu/Downloads/ipl data pipeline/silver/dim_teams.parquet")
print(df.columns.tolist())
df = pd.read_parquet("C:/Users/vishu/Downloads/ipl data pipeline/silver/dim_venues.parquet")
print(df.columns.tolist())