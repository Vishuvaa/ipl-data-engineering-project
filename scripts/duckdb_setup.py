import duckdb

# Create / Open Database
con = duckdb.connect(
    r"C:\Users\vishu\Downloads\ipl data pipeline\ipl.duckdb"
)

# ==========================
# Player Statistics
# ==========================

con.execute("""
CREATE OR REPLACE TABLE player_statistics AS
SELECT *
FROM read_parquet(
'C:/Users/vishu/Downloads/ipl data pipeline/gold/player_statistics.parquet'
)
""")

# ==========================
# Bowler Statistics
# ==========================

con.execute("""
CREATE OR REPLACE TABLE bowler_statistics AS
SELECT *
FROM read_parquet(
'C:/Users/vishu/Downloads/ipl data pipeline/gold/bowler_statistics.parquet'
)
""")

# ==========================
# Team Statistics
# ==========================

con.execute("""
CREATE OR REPLACE TABLE team_statistics AS
SELECT *
FROM read_parquet(
'C:/Users/vishu/Downloads/ipl data pipeline/gold/team_statistics.parquet'
)
""")

# ==========================
# Venue Statistics
# ==========================

con.execute("""
CREATE OR REPLACE TABLE venue_statistics AS
SELECT *
FROM read_parquet(
'C:/Users/vishu/Downloads/ipl data pipeline/gold/venue_statistics.parquet'
)
""")

# ==========================
# Season Statistics
# ==========================

con.execute("""
CREATE OR REPLACE TABLE season_statistics AS
SELECT *
FROM read_parquet(
'C:/Users/vishu/Downloads/ipl data pipeline/gold/season_statistics.parquet'
)
""")

print("DuckDB Database Created Successfully!")

print("\nTables:")

print(
    con.execute("SHOW TABLES").fetchdf()
)

con.close()