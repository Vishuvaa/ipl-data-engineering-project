import pandas as pd

df = pd.read_parquet("C:/Users/vishu/Downloads/ipl data pipeline/silver/fact_deliveries.parquet")

print(df.head())