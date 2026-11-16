from pathlib import Path

import pandas as pd

from purchasing_power.config import END, START


def standardize_month_col(df, col_name="month"):
    df1 = df.copy()
    df1[col_name] = pd.to_datetime(df1[col_name]).dt.to_period("M")
    return df1


def to_monthly_last_observation(df, date_col):
    df1 = df.copy()

    df1[date_col] = pd.to_datetime(df1[date_col])
    df1 = df1.sort_values(by=date_col)

    df1["month"] = df1[date_col].dt.to_period("M")  # extract months from dates
    df1 = df1.groupby("month").tail(1)  # make the data monthly

    df1 = df1.reset_index(drop=True)

    return df1


def build_monthly_min_wage(
    file_path=Path("data/reference/min_wage.csv"),
    start=START,
    end=END
):
    """
    Build a monthly minimum wage series for each sector.

    Each month receives the latest wage whose effective_date
    is less than or equal to that month.
    """

    # 1. Load data
    df = pd.read_csv(file_path)

    # 2. Standardize dates
    df["effective_date"] = pd.to_datetime(df["effective_date"])
    df["month"] = df["effective_date"].dt.to_period("M")

    # 3. Create monthly date range
    months = pd.period_range(start=start, end=end, freq="M")

    # 4. Create the output dataframe
    df_monthly = pd.DataFrame({"month": months})

    # 5. Build monthly wage series for each sector
    for sector in df["sector"].unique():

        sector_df = df[df["sector"] == sector].copy()

        sector_df = sector_df.sort_values("month")

        monthly_wages = []

        for month in months:

            eligible_wages = sector_df[
                sector_df["month"] <= month
            ]

            if eligible_wages.empty:
                monthly_wages.append(None)
            else:
                latest_wage = eligible_wages.iloc[-1]["amount_egp"]
                monthly_wages.append(latest_wage)

        df_monthly[sector] = monthly_wages

    return df_monthly
