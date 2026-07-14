import os
import pandas as pd

# =====================================
# Read Silver Layer
# =====================================

df = pd.read_parquet(
    r"C:\Users\vishu\Downloads\ipl data pipeline\silver\fact_deliveries.parquet"
)

# =====================================
# Group By Bowler
# =====================================

grouped = df.groupby("bowler")

# =====================================
# Innings Bowled
# =====================================

innings = (
    df[["bowler", "match_id", "innings"]]
    .drop_duplicates(subset=["bowler", "match_id", "innings"])
    .groupby("bowler")
    .size()
    .reset_index(name="innings")
)

# =====================================
# Balls Bowled
# (Only Legal Deliveries)
# =====================================

legal_df = df[df["legal_delivery"]]

balls = (
    legal_df.groupby("bowler")["legal_delivery"]
    .count()
    .reset_index()
    .rename(columns={"legal_delivery": "balls_bowled"})
)

# =====================================
# Runs Conceded
# =====================================

runs = (
    grouped["total_runs"]
    .sum()
    .reset_index()
    .rename(columns={"total_runs": "runs_conceded"})
)

# =====================================
# Bowler Wickets
# (Exclude Run Out, Retired Hurt, Obstructing the Field)
# =====================================

bowler_wickets_df = df[
    (df["is_wicket"]) &
    (~df["dismissal_type"].fillna("").isin([
        "run out",
        "retired hurt",
        "obstructing the field"
    ]))
]

wickets = (
    bowler_wickets_df.groupby("bowler")
    .size()
    .reset_index(name="wickets")
)

# =====================================
# Dot Balls
# =====================================

dot_df = legal_df[legal_df["total_runs"] == 0]

dot_balls = (
    dot_df.groupby("bowler")
    .size()
    .reset_index(name="dot_balls")
)

# =====================================
# Merge Everything
# =====================================

bowler_stats = (
    innings
    .merge(balls, on="bowler")
    .merge(runs, on="bowler")
    .merge(wickets, on="bowler")
    .merge(dot_balls, on="bowler", how="left")
)

# =====================================
# Fill Missing Dot Balls
# =====================================

bowler_stats["dot_balls"] = (
    bowler_stats["dot_balls"]
    .fillna(0)
    .astype(int)
)

# =====================================
# Overs Bowled
# =====================================

bowler_stats["overs"] = (
    bowler_stats["balls_bowled"] // 6
).astype(str) + "." + (
    bowler_stats["balls_bowled"] % 6
).astype(str)

# =====================================
# Economy
# =====================================

bowler_stats["economy"] = (
    bowler_stats["runs_conceded"] /
    (bowler_stats["balls_bowled"] / 6)
).round(2)

# =====================================
# Arrange Columns
# =====================================

bowler_stats = bowler_stats[
    [
        "bowler",
        "innings",
        "balls_bowled",
        "overs",
        "runs_conceded",
        "wickets",
        "dot_balls",
        "economy"
    ]
]

# =====================================
# Sort
# =====================================

bowler_stats = bowler_stats.sort_values(
    by="wickets",
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
# Save
# =====================================

bowler_stats.to_csv(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold\bowler_statistics.csv",
    index=False
)

bowler_stats.to_parquet(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold\bowler_statistics.parquet",
    index=False
)

# =====================================
# Summary
# =====================================

print("=" * 70)
print(bowler_stats.head(20))
print("=" * 70)

print(f"\nTotal Bowlers : {len(bowler_stats)}")

print("\nGold Layer - Bowler Statistics Created Successfully!")