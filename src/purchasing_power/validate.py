import pandas as pd


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