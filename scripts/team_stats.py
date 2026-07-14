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
# Runs Scored
# =====================================

runs_scored = (
    deliveries.groupby("batting_team")["total_runs"]
    .sum()
    .reset_index()
    .rename(columns={
        "batting_team": "team",
        "total_runs": "runs_scored"
    })
)

# =====================================
# Runs Conceded
# =====================================

runs_conceded = (
    deliveries.groupby("bowling_team")["total_runs"]
    .sum()
    .reset_index()
    .rename(columns={
        "bowling_team": "team",
        "total_runs": "runs_conceded"
    })
)

# =====================================
# Matches Played
# =====================================

team1 = matches[["team1"]].rename(columns={"team1": "team"})
team2 = matches[["team2"]].rename(columns={"team2": "team"})

all_matches = pd.concat([team1, team2])

matches_played = (
    all_matches.groupby("team")
    .size()
    .reset_index(name="matches")
)

# =====================================
# Wins
# =====================================

wins = (
    matches.dropna(subset=["winner"])
    .groupby("winner")
    .size()
    .reset_index(name="wins")
    .rename(columns={"winner": "team"})
)

# =====================================
# Toss Wins
# =====================================

toss = (
    matches.groupby("toss_winner")
    .size()
    .reset_index(name="toss_wins")
    .rename(columns={"toss_winner": "team"})
)

# =====================================
# Merge
# =====================================

team_stats = (
    matches_played
    .merge(wins, on="team", how="left")
    .merge(toss, on="team", how="left")
    .merge(runs_scored, on="team", how="left")
    .merge(runs_conceded, on="team", how="left")
)

# =====================================
# Fill Missing Values
# =====================================

team_stats["wins"] = team_stats["wins"].fillna(0).astype(int)
team_stats["toss_wins"] = team_stats["toss_wins"].fillna(0).astype(int)
team_stats["runs_scored"] = team_stats["runs_scored"].fillna(0).astype(int)
team_stats["runs_conceded"] = team_stats["runs_conceded"].fillna(0).astype(int)

# =====================================
# Losses
# =====================================

team_stats["losses"] = (
    team_stats["matches"] - team_stats["wins"]
)

# =====================================
# Win Percentage
# =====================================

team_stats["win_percentage"] = (
    team_stats["wins"]
    / team_stats["matches"]
    * 100
).round(2)

# =====================================
# Arrange Columns
# =====================================

team_stats = team_stats[
    [
        "team",
        "matches",
        "wins",
        "losses",
        "toss_wins",
        "runs_scored",
        "runs_conceded",
        "win_percentage"
    ]
]

# =====================================
# Sort
# =====================================

team_stats = team_stats.sort_values(
    by="wins",
    ascending=False
).reset_index(drop=True)

# =====================================
# Save
# =====================================

os.makedirs(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold",
    exist_ok=True
)

team_stats.to_csv(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold\team_statistics.csv",
    index=False
)

team_stats.to_parquet(
    r"C:\Users\vishu\Downloads\ipl data pipeline\gold\team_statistics.parquet",
    index=False
)

# =====================================
# Summary
# =====================================

print("=" * 70)
print(team_stats)
print("=" * 70)

print(f"\nTotal Teams : {len(team_stats)}")

print("\nGold Layer - Team Statistics Created Successfully!")