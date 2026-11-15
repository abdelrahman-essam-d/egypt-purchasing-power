from pathlib import Path

import pandas as pd

from purchasing_power.config import END, START
from purchasing_power.transform import standardize_month_col
from purchasing_power.validate import validate_dataset


def load_datasets() -> dict:

    print("Data integration process is starting ...")

    data_dir = Path("data/processed")
    files = {
        "cpi": "cpi_egypt_monthly.csv",
        "usd": "usd_egp_monthly.csv",
        "gold_local": "gold_egypt_egp_monthly.csv",
        "gold_global": "gold_world_usd_monthly.csv",
    }

    # check if data exists
    for file_name in files.values():
        path = data_dir / file_name
        if not path.exists():
            raise FileNotFoundError(f"file does not exist ! {path}")

    # data reading and standerdize month column data type

    print("reading and standerdizing month column in files ...")

    df_cpi = pd.read_csv(data_dir / files["cpi"])
    df_usd = pd.read_csv(data_dir / files["usd"])
    df_gold_local = pd.read_csv(data_dir / files["gold_local"])
    df_gold_global = pd.read_csv(data_dir / files["gold_global"])

    df_cpi = standardize_month_col(df_cpi)
    df_usd = standardize_month_col(df_usd)
    df_gold_local = standardize_month_col(df_gold_local)
    df_gold_global = standardize_month_col(df_gold_global)

    return {
        "cpi": df_cpi,
        "usd": df_usd,
        "gold_local": df_gold_local,
        "gold_global": df_gold_global,
    }


def merge_datasets(
    datasets: dict, output_path: Path = Path("data/processed/economic_indicators_monthly.csv")
) -> pd.DataFrame:

    df_cpi = datasets["cpi"]
    df_usd = datasets["usd"]  # extract datasets
    df_gold_local = datasets["gold_local"]
    df_gold_global = datasets["gold_global"]

    # start outer merging
    print("start merging ...")

    df_merged = pd.merge(df_cpi, df_usd, on="month", how="outer", suffixes=("", "_usd"))
    df_merged = pd.merge(
        df_merged, df_gold_local, on="month", how="outer", suffixes=("", "_gold_local")
    )
    df_merged = pd.merge(
        df_merged, df_gold_global, on="month", how="outer", suffixes=("", "_gold_world")
    )

    # Not important columns
    columns_to_drop = {
        "source",
        "date",
        "base",
        "quote",
        "obs_date",
        "source_gold_local",
        "note",
        "source_gold_world",
        "note_gold_world",
    }

    df_merged = df_merged.drop(columns=columns_to_drop, errors="ignore")

    df_merged = df_merged.rename(columns={"rate": "egp_per_usd"})

    df_merged = df_merged.sort_values("month").reset_index(drop=True)

    missing_rows = df_merged.loc[df_merged["egp_per_usd"].isna(), "month"]
    print(missing_rows)

    df_merged["month_period"] = pd.to_datetime(df_merged["month"]).dt.to_period("M")
    df_merged = df_merged[
        (df_merged["month_period"] >= pd.Period(START, freq="M"))
        & (df_merged["month_period"] <= pd.Period(END, freq="M"))
    ]
    df_merged = df_merged.drop(columns=["month_period"]).reset_index(drop=True)

    validate_dataset(
        df_merged,
        month_col="month",
        value_cols=["cpi_index", "egp_per_usd", "gold24_egp_per_gram", "gold_usd_per_oz"],
        start=START,
        end=END,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_merged.to_csv(output_path, index=False)

    print(f"\n successfully saved merged dataset to: {output_path}")
    print(f"total rows: {len(df_merged)}")
    print(f"date range: from {df_merged['month'].min()} to {df_merged['month'].max()}")

    return df_merged


def update_usd_dataset(
    base_path: Path = Path("data/processed/usd_egp_monthly.csv"),
    new_path: Path = Path("data/processed/usd_egp_monthly_were_missing.csv"),
) -> pd.DataFrame:

    print("Processing ...")

    if not base_path.exists():
        raise FileNotFoundError(f"This file does not exist in this path -> {base_path}")
    if not new_path.exists():
        raise FileNotFoundError(f"This file does not exist in this path -> {new_path}")

    df_base = pd.read_csv(base_path)
    df_new = pd.read_csv(new_path)

    if "month" not in df_base.columns or "month" not in df_new.columns:
        raise ValueError("Missing month column")

    df_combined = pd.concat([df_base, df_new], ignore_index=True)  # merge

    df_combined = df_combined.drop_duplicates(subset=["month"], keep="last")
    df_combined = df_combined.sort_values("month").reset_index(drop=True)

    df_combined.to_csv(base_path, index=False)

    print(f"\nSuccessfully updated USD dataset and saved to: {base_path}")
    print(f"Total rows after update: {len(df_combined)}")
    print(f"Date range: from {df_combined['month'].min()} to {df_combined['month'].max()}")

    return df_combined


if __name__ == "__main__":
    datasets = load_datasets()
    df_merged = merge_datasets(datasets)
