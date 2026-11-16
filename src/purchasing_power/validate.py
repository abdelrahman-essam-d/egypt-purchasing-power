from pathlib import Path

import pandas as pd

from purchasing_power.config import END, START


def check_missing_or_duplicate_months(df, month_col="month", start=None, end=None):
    if df.empty:
        raise ValueError("DataFrame is empty.")
    if month_col not in df.columns:
        raise KeyError(f"Month column '{month_col}' not found in DataFrame.")

    # 1. unify data type
    df_temp = df.copy()
    df_temp[month_col] = pd.to_datetime(df_temp[month_col]).dt.to_period("M")

    # 2. check chronological order (sorted ascending)
    if not df_temp[month_col].is_monotonic_increasing:
        raise ValueError("Months are not sorted in chronological (ascending) order.")

    # 3. check duplicates
    if df_temp[month_col].duplicated().any():
        duplicates = df_temp[df_temp[month_col].duplicated()][month_col].astype(str).tolist()
        raise ValueError(f"Duplicate months found: {duplicates}")

    # 4. determine the scope and missing months
    min_month = df_temp[month_col].min()
    max_month = df_temp[month_col].max()

    # 5. check boundaries (start & end)
    if start is not None and pd.Period(start, freq="M") != min_month:
        raise ValueError(f"Start month mismatch: expected {start}, but got {min_month}")

    if end is not None and pd.Period(end, freq="M") != max_month:
        raise ValueError(f"End month mismatch: expected {end}, but got {max_month}")

    full_range = pd.period_range(start=min_month, end=max_month, freq="M")
    existing_months = set(df_temp[month_col])
    missing_months = [str(m) for m in full_range if m not in existing_months]

    if missing_months:
        raise ValueError(f"Missing months found between range: {missing_months}")

    return True


def check_positive_values(df, col_name):
    if df.empty:
        raise ValueError("DataFrame is empty.")
    if col_name not in df.columns:
        raise KeyError(f"Column '{col_name}' not found in DataFrame.")

    # 1. check nan values
    missing_rows = df[df[col_name].isna()].index.tolist()
    if missing_rows:
        raise ValueError(f"Found missing (NaN) values at row indices: {missing_rows}")
    
    # 2. check invalid values
    invalid_mask = df[col_name] <= 0
    if invalid_mask.any():
        invalid_data = df[invalid_mask][col_name]
        details = {idx: val for idx, val in invalid_data.items()}
        raise ValueError(f"Found non-positive values (<= 0) at row indices and values: {details}")

    return True


def validate_dataset(df, month_col="month", value_cols=None, start=None, end=None):
    if value_cols is None:
        value_cols = []

    if df.empty:
        raise ValueError("DataFrame is empty.")

    # 1. check columns existence
    if month_col not in df.columns:
        raise KeyError(f"Month column '{month_col}' not found in DataFrame.")
    for col in value_cols:
        if col not in df.columns:
            raise KeyError(f"Value column '{col}' not found in DataFrame.")

    # 2. check nans across columns
    if df.isna().any().any():
        na_cols = df.columns[df.isna().any()].tolist()
        raise ValueError(f"Found missing (NaN) values in columns: {na_cols}")

    # 3. check_missing_or_duplicate_months (passing start and end)
    check_missing_or_duplicate_months(df, month_col=month_col, start=start, end=end)

    # 4. check_positive_values
    for col in value_cols:
        check_positive_values(df, col)

    return True





def validate_reference_tables(
    min_wage_path: Path = Path("data/reference/min_wage.csv"),
    events_path: Path = Path("data/reference/events.csv")
) -> bool:
    
    # Check files and its content
    if not min_wage_path.exists():
        raise FileNotFoundError(f"min_wage file not found at: {min_wage_path}")
    if not events_path.exists():
        raise FileNotFoundError(f"events file not found at: {events_path}")

    df_mw = pd.read_csv(min_wage_path)
    df_events = pd.read_csv(events_path)

    if df_mw.empty:
        raise ValueError("min_wage table is empty.")
    if df_events.empty:
        raise ValueError("events table is empty.")

    # Check requaired columns existance
    required_mw_cols = ["sector", "effective_date", "amount_egp", "confidence"]
    for col in required_mw_cols:
        if col not in df_mw.columns:
            raise KeyError(f"Missing required column '{col}' in min_wage.csv")

    required_event_cols = [
        "event_id", "event_date", "month", "type", "description",
        "fx_before_egp_per_usd", "fx_after_egp_per_usd",
        "policy_rate_change_bp", "source_1", "source_2", "confidence", "note"
    ]
    for col in required_event_cols:
        if col not in df_events.columns:
            raise KeyError(f"Missing required column '{col}' in events.csv")

    # Check invalid values in sector
    if df_mw["sector"].isna().any():
        raise ValueError("Found missing (NaN) values in min_wage 'sector'.")
    if df_mw["sector"].astype(str).str.strip().eq("").any():
        raise ValueError("Found empty or whitespace values in min_wage 'sector'.")

    # Checking acceptability of transforming dates
    df_mw["parsed_effective_date"] = pd.to_datetime(df_mw["effective_date"], errors="coerce")
    if df_mw["parsed_effective_date"].isna().any():
        raise ValueError("Found missing, empty, or invalid date values (NaT) in min_wage 'effective_date'.")

    df_events["parsed_event_date"] = pd.to_datetime(df_events["event_date"], errors="coerce")
    if df_events["parsed_event_date"].isna().any():
        raise ValueError("Found missing, empty, or invalid date values (NaT) in events 'event_date'.")

    # Check for invalid or NaN values in "amount_egp" column
    converted_amount = pd.to_numeric(df_mw["amount_egp"], errors="coerce")
    if converted_amount.isna().any():
        bad_indices = df_mw[converted_amount.isna()].index.tolist()
        raise ValueError(f"Found missing, non-numeric, or invalid values in min_wage 'amount_egp' at indices: {bad_indices}")
    
    df_mw["amount_egp"] = converted_amount

    invalid_amounts = df_mw[df_mw["amount_egp"] <= 0]
    if not invalid_amounts.empty:
        details = {idx: val for idx, val in invalid_amounts["amount_egp"].items()}
        raise ValueError(f"Found non-positive values (<= 0) in min_wage 'amount_egp' at indices: {details}")

    # Checking confidance
    valid_confidences = {"high", "medium", "low"}
    if df_mw["confidence"].isna().any():
        raise ValueError("Found missing (NaN) values in min_wage 'confidence'.")
    
    invalid_conf = df_mw[~df_mw["confidence"].isin(valid_confidences)]
    if not invalid_conf.empty:
        unique_bad = invalid_conf["confidence"].unique()
        raise ValueError(f"Invalid confidence values in min_wage: {unique_bad}. Must be one of {valid_confidences}")

    if df_events["confidence"].isna().any():
        raise ValueError("Found missing (NaN) values in events 'confidence'.")
    
    invalid_event_conf = df_events[~df_events["confidence"].isin(valid_confidences)]
    if not invalid_event_conf.empty:
        unique_bad_event = invalid_event_conf["confidence"].unique()
        raise ValueError(f"Invalid confidence values in events: {unique_bad_event}. Must be one of {valid_confidences}")

    # Check duplicates in sector date
    if df_mw.duplicated(subset=["sector", "parsed_effective_date"]).any():
        duplicates = df_mw[df_mw.duplicated(subset=["sector", "parsed_effective_date"], keep=False)]
        dup_details = duplicates[["sector", "effective_date"]].to_dict(orient="records")
        raise ValueError(f"Duplicate effective dates found within the same sector: {dup_details}")

    # Checking chronological order and non reduction of wages in sectors
    for sector, group in df_mw.groupby("sector"):
        if not group["parsed_effective_date"].is_monotonic_increasing:
            raise ValueError(f"Effective dates for sector '{sector}' are not sorted in chronological order in the raw data.")

    df_mw_sorted = df_mw.sort_values(by=["sector", "parsed_effective_date"])
    for sector, group in df_mw_sorted.groupby("sector"):
        if not group["amount_egp"].is_monotonic_increasing:
            raise ValueError(f"Wage amounts for sector '{sector}' decrease over time (violation of non-decreasing rule).")

    # Checking START and END
    start_period = pd.Period(START, freq="M")
    end_period = pd.Period(END, freq="M")

    df_events["event_period"] = df_events["parsed_event_date"].dt.to_period("M")
    outside_events = df_events[
        (df_events["event_period"] < start_period) | (df_events["event_period"] > end_period)
    ]

    if not outside_events.empty:
        bad_dates = outside_events["event_date"].tolist()
        raise ValueError(f"Events found outside the allowed period [{START} to {END}]: {bad_dates}")

    print("Reference tables validation PASSED successfully!")
    return True






