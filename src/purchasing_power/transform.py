
import pandas as pd



def standardize_month_col (df, col_name="month"):
    df1 = df.copy()
    df1[col_name] = pd.to_datetime(df1[col_name]).dt.to_period("M") 
    return df1


def to_monthly_last_observation (df, date_col):
    df1 = df.copy()

    df1[date_col] = pd.to_datetime(df1[date_col])
    df1 = df1.sort_values(by=date_col)

    df1["month"] = df1[date_col].dt.to_period("M")     # extract months from dates
    df1 = df1.groupby("month").tail(1)               # make the data monthly

    df1 = df1.reset_index(drop=True)

    return df1




