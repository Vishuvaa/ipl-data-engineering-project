import duckdb

con = duckdb.connect(
    r"C:\Users\vishu\Downloads\ipl data pipeline\ipl.duckdb"
)

print(con.execute("DESCRIBE player_statistics").fetchdf())
query = """
SELECT
    batter,
    total_runs,
    strike_rate
FROM player_statistics
ORDER BY total_runs DESC
LIMIT 10;
"""

df = con.execute(query).fetchdf()

print(df)

con.close()