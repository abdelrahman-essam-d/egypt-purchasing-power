import os

import pandas as pd

from purchasing_power.config import END, START
from purchasing_power.validate import validate_dataset, validate_reference_tables

datasets_config = {
    "cpi_egypt_monthly.csv": {"month_col": "month", "value_cols": ["cpi_index"]},
    "usd_egp_monthly.csv": {"month_col": "month", "value_cols": ["rate"]},
    "gold_egypt_egp_monthly.csv": {
        "month_col": "month",
        "value_cols": ["gold24_egp_per_gram"],
    },
    "gold_world_usd_monthly.csv": {
        "month_col": "month",
        "value_cols": ["gold_usd_per_oz"],
    },
}

print("Starting automated datasets validation..\n")

for filename, config in datasets_config.items():
    print(f"Checking file: {filename} ... ", end="")

    file_path = os.path.join("data/processed", filename)

    if not os.path.exists(file_path):
        print("FAILED: File not found!")
        continue

    try:
        df = pd.read_csv(file_path)

        validate_dataset(
            df, month_col=config["month_col"], value_cols=config["value_cols"], start=START, end=END
        )

        print("PASSED")
    except Exception as e:  # noqa: BLE001
        print(f"FAILED\n  Reason: {e}\n")

print("\n Validation process completed.")







if __name__ == "__main__":
    validate_reference_tables()