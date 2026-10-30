
import pandas as pd
import pytest
from purchasing_power.transform import to_monthly_last_observation
from purchasing_power.transform import standardize_month_col


def test_to_monthly_last_observation():
    data = {
        'date': ['2026-01-05', '2026-01-15', '2026-01-31', '2026-02-10', '2026-02-28'],
            'rate': [47.5, 48.0, 49.0, 50.0, 51.0]
    }
    df = pd.DataFrame(data)

    result = to_monthly_last_observation(df, date_col="date")

    assert len(result) == 2
    assert result.loc[0, "rate"] == 49.0
    assert result.loc[1, "rate"] == 51.0

def test_to_monthly_last_observation_does_not_modify_original():

    data = {
        'date': ['2026-01-05', '2026-01-15', '2026-01-31', '2026-02-10', '2026-02-28'],
        'rate': [47.5, 48.0, 49.0, 50.0, 51.0]
    }
    df = pd.DataFrame(data)
    
    df_original = df.copy()
    
    result = to_monthly_last_observation(df, "date")
    
    pd.testing.assert_frame_equal(df, df_original)    

def test_to_monthly_last_observation_unsorted_data ():

    data = {
        "date": ["2026-01-31", "2026-01-05", "2026-01-15"],
        "rate": [49.0, 47.5, 48.0]
    }
    df = pd.DataFrame(data)

    result = to_monthly_last_observation(df, "date")
    assert len(result) == 1         
    assert result.loc[0, "rate"] == 49.0
    assert str(result.loc[0, "month"]) == "2026-01"

def test_to_monthly_last_observation_no_duplicate_months():
    data = {
        'date': ['2026-01-02', '2026-01-15', '2026-01-31', '2026-02-05', '2026-02-20'],
        'rate': [47.0, 48.0, 49.0, 50.0, 51.0]
    }
    df = pd.DataFrame(data)
    
    result = to_monthly_last_observation(df, date_col="date")
    
    assert len(result) == result['month'].nunique()
    assert not result['month'].duplicated().any()    



def test_to_monthly_last_observation_missing_date_column():
    data = {
        'wrong_date_col': ['2026-01-05', '2026-01-15'],
        'rate': [47.5, 48.0]
    }
    df = pd.DataFrame(data)
    
    with pytest.raises(KeyError):
        to_monthly_last_observation(df, date_col="date")    


def test_standardize_month_col_type():
    data = {
        'month': ['2026-01-05', '2026-01-20', '2026-02-15']
    }
    df = pd.DataFrame(data)
    
    result_df = standardize_month_col(df, col_name='month')
    
    assert str(result_df['month'].dtype) == 'period[M]'


def test_standardize_month_col_values():
    data = {
        'month': ['2026-01-05', '2026-01-20', '2026-02-15']
    }
    df = pd.DataFrame(data)
    
    result_df = standardize_month_col(df, col_name='month')
    
    assert str(result_df.loc[0, 'month']) == '2026-01'
    assert str(result_df.loc[1, 'month']) == '2026-01'
    assert str(result_df.loc[2, 'month']) == '2026-02'