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
        ["match_id", "innings"]
    )
    .agg(
        innings_runs=("total_runs", "sum"),
        innings_wickets=("is_wicket", "sum")
    )
    .reset_index()
)

# Add Year

innings_summary = innings_summary.merge(
    matches[["match_id", "year"]],
    on="match_id"
)

# =====================================
# Season Statistics
# =====================================

season_stats = (
    innings_summary.groupby("year")
    .agg(
        matches=("match_id", "nunique"),
        highest_score=("innings_runs", "max"),
        average_score=("innings_runs", "mean")
    )
    .reset_index()
)

# =====================================
# Total Runs
# =====================================

runs = (
    deliveries.merge(
        matches[["match_id", "year"]],
        on="match_id"
    )
    .groupby("year")["total_runs"]
    .sum()
    .reset_index(name="total_runs")
)

# =====================================
# Total Wickets
# =====================================

wickets = (
    deliveries.merge(
        matches[["match_id", "year"]],
        on="match_id"
    )
    .groupby("year")["is_wicket"]
    .sum()
    .reset_index(name="total_wickets")
)

# =====================================
# Total Fours
# =====================================

fours = (
    deliveries.merge(
        matches[["match_id", "year"]],
        on="match_id"
    )
    .groupby("year")["is_four"]
    .sum()
    .reset_index(name="fours")
)

# =====================================
# Total Sixes
# =====================================

sixes = (
    deliveries.merge(
        matches[["match_id", "year"]],
        on="match_id"
    )
    .groupby("year")["is_six"]
    .sum()
    .reset_index(name="sixes")
)

# =====================================
# Merge Everything
# =====================================

season_stats = (
    season_stats
    .merge(runs, on="year")
    .merge(wickets, on="year")
    .merge(fours, on="year")
    .merge(sixes, on="year")
)

# =====================================
# Round
# =====================================

season_stats["average_score"] = (
    season_stats["average_score"]
    .round(2)
)

# =====================================
# Arrange Columns
# =====================================

season_stats = season_stats[
    [
        "year",
        "matches",
        "total_runs",
        "total_wickets",
        "fours",
        "sixes",
        "average_score",
        "highest_score"
    ]
]

# =====================================
# Sort
# =====================================

season_stats = season_stats.sort_values(
    by="year"
).reset_index(drop=True)

# =====================================
# Save
# =====================================

os.makedirs(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold",
    exist_ok=True
)

season_stats.to_csv(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold\season_statistics.csv",
    index=False
)

season_stats.to_parquet(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold\season_statistics.parquet",
    index=False
)

# =====================================
# Output
# =====================================

print("=" * 80)
print(season_stats)
print("=" * 80)

print(f"\nTotal Seasons : {len(season_stats)}")

print("\nGold Layer - Season Statistics Created Successfully!")