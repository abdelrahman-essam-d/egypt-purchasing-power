

from pathlib import Path

import duckdb


def create_database(
    db_path=Path("data/analytics/purchasing_power.duckdb"),
    data_dir=Path("data"),
):
    """
    Create DuckDB database and load project datasets.
    """

    print("Starting DuckDB database creation...")

    # Create database directory
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Define source files
    datasets = {
        "economic_indicators": (
            data_dir / "processed/economic_indicators_monthly.csv"
        ),
        "minimum_wage": (
            data_dir / "processed/min_wage_monthly.csv"
        ),
        "real_wages": (
            data_dir / "processed/real_min_wage_monthly.csv"
        ),
        "wage_recovery": (
            data_dir / "processed/wage_recovery.csv"
        ),
        "implied_fx": (
            data_dir / "processed/implied_fx_monthly.csv"
        ),
        "events": (
            data_dir / "reference/events.csv"
        ),
    }

    # Connect to database
    conn = duckdb.connect(str(db_path))

    try:
        for table_name, file_path in datasets.items():

            if not file_path.exists():
                raise FileNotFoundError(
                    f"Dataset not found: {file_path}"
                )

            csv_path = str(file_path.resolve()).replace("'", "''")

            conn.execute(
                f"""
                CREATE OR REPLACE TABLE {table_name} AS
                SELECT *
                FROM read_csv_auto('{csv_path}')
                """
            )

            row_count = conn.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]

            print(
                f"{table_name}: {row_count} rows loaded"
            )

    finally:
        conn.close()

    print("\nDuckDB database created successfully!")


if __name__ == "__main__":
    create_database()
