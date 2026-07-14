import duckdb

# Create connection
con = duckdb.connect()

# Install and load S3 extension
con.execute("INSTALL httpfs;")
con.execute("LOAD httpfs;")

# Use AWS CLI credentials
con.execute("""
CREATE OR REPLACE SECRET aws_secret (
    TYPE S3,
    PROVIDER CREDENTIAL_CHAIN
);
""")

# Read directly from S3
df = con.execute("""
SELECT *
FROM read_parquet(
's3://vishuvaa-ipl-de-project-339712865765-ap-south-1-an/gold/player_statistics.parquet'
)
LIMIT 10;
""").fetchdf()

print(df)

con.close()