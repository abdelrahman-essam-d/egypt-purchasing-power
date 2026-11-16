import duckdb

conn = duckdb.connect(
    "data/analytics/purchasing_power.duckdb"
)

tables = conn.execute("SHOW TABLES").fetchdf()

print(tables)

conn.close()