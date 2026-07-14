import os
import pandas as pd

# =====================================
# Read Silver Layer
# =====================================

deliveries = pd.read_parquet(
    r"C:\Users\vishu\Downloads\ipl data pipeline\silver\fact_deliveries.parquet"
)

matches = pd.read_parquet(
    r"C:\Users\vishu\Downloads\ipl data pipeline\silver\dim_matches.parquet"
)

# =====================================
# Create Innings Summary
# =====================================

innings_summary = (
    deliveries.groupby(
        ["match_id", "innings", "batting_team", "bowling_team"]
    )
    .agg(
        total_runs=("total_runs", "sum"),
        wickets=("is_wicket", "sum")
    )
    .reset_index()
)
print(innings_summary.head())
print(len(innings_summary))

# =====================================
# Merge Venue
# =====================================

innings_summary = innings_summary.merge(
    matches[["match_id", "venue", "winner"]],
    on="match_id"
)
print(innings_summary.head())
print(len(innings_summary))
# =====================================
# Batting First Team
# =====================================

first_innings = innings_summary[
    innings_summary["innings"] == 1
][["match_id", "batting_team"]]

first_innings.rename(
    columns={"batting_team": "batting_first_team"},
    inplace=True
)

innings_summary = innings_summary.merge(
    first_innings,
    on="match_id"
)
print(len(innings_summary))

# =====================================
# Chasing Team
# =====================================

second_innings = innings_summary[
    innings_summary["innings"] == 2
][["match_id", "batting_team"]]

second_innings.rename(
    columns={"batting_team": "chasing_team"},
    inplace=True
)

innings_summary = innings_summary.merge(
    second_innings,
    on="match_id"
)
print(len(innings_summary))

# =====================================
# Flags
# =====================================

innings_summary["batting_first_win"] = (
    innings_summary["winner"]
    == innings_summary["batting_first_team"]
)

innings_summary["chasing_win"] = (
    innings_summary["winner"]
    == innings_summary["chasing_team"]
)

# =====================================
# Venue Statistics
# =====================================

venue_stats = (
    innings_summary.groupby("venue")
    .agg(
        matches=("match_id", "nunique"),
        innings=("innings", "count"),
        highest_score=("total_runs", "max"),
        lowest_score=("total_runs", "min")
    )
    .reset_index()
)

# =====================================
# Average 1st Innings Score
# =====================================

avg_first = (
    innings_summary[
        innings_summary["innings"] == 1
    ]
    .groupby("venue")["total_runs"]
    .mean()
    .reset_index(name="average_1st_innings")
)

# =====================================
# Average 2nd Innings Score
# =====================================

avg_second = (
    innings_summary[
        innings_summary["innings"] == 2
    ]
    .groupby("venue")["total_runs"]
    .mean()
    .reset_index(name="average_2nd_innings")
)

# =====================================
# Batting First Win %
# =====================================

bat_first = (
    innings_summary[
        innings_summary["innings"] == 1
    ]
    .groupby("venue")["batting_first_win"]
    .mean()
    .reset_index(name="batting_first_win_percentage")
)

bat_first["batting_first_win_percentage"] *= 100

# =====================================
# Chasing Win %
# =====================================

chasing = (
    innings_summary[
        innings_summary["innings"] == 2
    ]
    .groupby("venue")["chasing_win"]
    .mean()
    .reset_index(name="chasing_win_percentage")
)

chasing["chasing_win_percentage"] *= 100

# =====================================
# Merge Everything
# =====================================

venue_stats = (
    venue_stats
    .merge(avg_first, on="venue")
    .merge(avg_second, on="venue")
    .merge(bat_first, on="venue")
    .merge(chasing, on="venue")
)

# =====================================
# Round
# =====================================

venue_stats["average_1st_innings"] = (
    venue_stats["average_1st_innings"]
    .round(2)
)

venue_stats["average_2nd_innings"] = (
    venue_stats["average_2nd_innings"]
    .round(2)
)

venue_stats["batting_first_win_percentage"] = (
    venue_stats["batting_first_win_percentage"]
    .round(2)
)

venue_stats["chasing_win_percentage"] = (
    venue_stats["chasing_win_percentage"]
    .round(2)
)

# =====================================
# Sort
# =====================================

venue_stats = venue_stats.sort_values(
    by="matches",
    ascending=False
).reset_index(drop=True)

# =====================================
# Save
# =====================================

os.makedirs(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold",
    exist_ok=True
)

venue_stats.to_csv(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold\venue_statistics.csv",
    index=False
)

venue_stats.to_parquet(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold\venue_statistics.parquet",
    index=False
)

# =====================================
# Output
# =====================================

print("=" * 80)
print(venue_stats)
print("=" * 80)

print(f"\nTotal Venues : {len(venue_stats)}")

print("\nGold Layer - Venue Statistics Created Successfully!")