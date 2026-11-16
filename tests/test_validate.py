
import pandas as pd
import pytest

from purchasing_power.config import END, START
from purchasing_power.validate import (
    check_missing_or_duplicate_months,
    check_positive_values,
    validate_dataset,
    validate_reference_tables,
)


def test_validate_dataset_end_mismatch():
    # إنشاء بيانات تبدأ من START الصحيح، ولكن تنتهي مبكراً قبل تاريخ END
    months = [str(m) for m in pd.period_range(start=START, end="2023-02", freq="M")]
    df_invalid = pd.DataFrame({
        "month": months,
        "val": [100.0] * len(months),
    })

    # التأكد من أن الدالة تفشل وترفع ValueError بسبب اختلاف تاريخ النهاية
    with pytest.raises(ValueError, match="End month mismatch"):
        validate_dataset(
            df_invalid,
            month_col="month",
            value_cols=["val"],
            start=START,
            end=END,
        )

def test_missing_months():

    df = pd.DataFrame({"month": ["2026-01", "2026-03"]})

    with pytest.raises(ValueError, match="Missing months found"):
        check_missing_or_duplicate_months(df, month_col="month")


def test_duplicate_months():

    df = pd.DataFrame({"month": ["2026-01", "2026-02", "2026-02"]})

    with pytest.raises(ValueError, match="Duplicate months found"):
        check_missing_or_duplicate_months(df, month_col="month")


def test_valid_consecutive_months():

    df = pd.DataFrame({"month": ["2026-01", "2026-02", "2026-03"]})

    result = check_missing_or_duplicate_months(df, month_col="month")
    assert result is True


def test_positive_values_valid():

    df = pd.DataFrame({"rate": [18.5, 19.2, 25.0]})

    result = check_positive_values(df, "rate")
    assert result is True


def test_positive_values_invalid():

    df = pd.DataFrame({"rate": [18.5, 0.0, -1.5]})

    with pytest.raises(ValueError, match="non-positive values"):
        check_positive_values(df, "rate")



def test_validate_empty_dataframe():
    """التحقق من رفض الـ DataFrame الفارغ برساْل واضح."""
    df_empty = pd.DataFrame()
    with pytest.raises(ValueError, match="DataFrame is empty"):
        check_missing_or_duplicate_months(df_empty)
    with pytest.raises(ValueError, match="DataFrame is empty"):
        validate_dataset(df_empty)


def test_validate_missing_columns():
    df = pd.DataFrame({"wrong_month": ["2023-01", "2023-02"], "val": [100.0, 105.0]})
    
    with pytest.raises(KeyError, match="Month column 'month' not found"):
        check_missing_or_duplicate_months(df, month_col="month")
    
    with pytest.raises(KeyError, match="Value column 'missing_col' not found"):
        validate_dataset(df, month_col="wrong_month", value_cols=["missing_col"])


def test_validate_unsorted_months():
    df_unsorted = pd.DataFrame({
        "month": ["2023-03", "2023-01", "2023-02"],
        "val": [100.0, 105.0, 110.0]
    })
    with pytest.raises(ValueError, match="not sorted in chronological"):
        check_missing_or_duplicate_months(df_unsorted)




VALID_EVENTS_CSV = (
    "event_id,event_date,month,type,description,fx_before_egp_per_usd,fx_after_egp_per_usd,"
    "policy_rate_change_bp,source_1,source_2,confidence,note\n"
    "E01,2020-01-01,2020-01,rate,test,30,30,100,src1,,high,test\n"
)


def test_validate_reference_tables_success(tmp_path):
    mw_file = tmp_path / "min_wage.csv"
    events_file = tmp_path / "events.csv"

    mw_data = "sector,effective_date,amount_egp,confidence\ngov,2020-01-01,2000,high\ngov,2022-01-01,2400,medium\n"
    mw_file.write_text(mw_data, encoding="utf-8")
    events_file.write_text(VALID_EVENTS_CSV, encoding="utf-8")

    assert validate_reference_tables(min_wage_path=mw_file, events_path=events_file) is True


def test_validate_reference_tables_file_not_found(tmp_path):
    non_existent = tmp_path / "non_existent.csv"
    valid_file = tmp_path / "events.csv"
    valid_file.write_text(VALID_EVENTS_CSV, encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        validate_reference_tables(min_wage_path=non_existent, events_path=valid_file)


def test_validate_reference_tables_invalid_date(tmp_path):
    mw_file = tmp_path / "min_wage.csv"
    events_file = tmp_path / "events.csv"

    mw_data = "sector,effective_date,amount_egp,confidence\ngov,invalid-date,2000,high\n"
    mw_file.write_text(mw_data, encoding="utf-8")
    events_file.write_text(VALID_EVENTS_CSV, encoding="utf-8")

    with pytest.raises(ValueError, match="invalid date values"):
        validate_reference_tables(min_wage_path=mw_file, events_path=events_file)


def test_validate_reference_tables_zero_amount(tmp_path):
    """اختبار رفع ValueError عندما يكون مبلغ الأجر يساوي صفرًا أو قيمة غير موجبة."""
    mw_file = tmp_path / "min_wage.csv"
    events_file = tmp_path / "events.csv"

    mw_data = "sector,effective_date,amount_egp,confidence\ngov,2020-01-01,0,high\n"
    mw_file.write_text(mw_data, encoding="utf-8")
    events_file.write_text(VALID_EVENTS_CSV, encoding="utf-8")

    with pytest.raises(ValueError, match="non-positive values"):
        validate_reference_tables(min_wage_path=mw_file, events_path=events_file)


def test_validate_reference_tables_invalid_confidence(tmp_path):
    mw_file = tmp_path / "min_wage.csv"
    events_file = tmp_path / "events.csv"

    mw_data = "sector,effective_date,amount_egp,confidence\ngov,2020-01-01,2000,unknown_conf\n"
    mw_file.write_text(mw_data, encoding="utf-8")
    events_file.write_text(VALID_EVENTS_CSV, encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid confidence values"):
        validate_reference_tables(min_wage_path=mw_file, events_path=events_file)


def test_validate_reference_tables_duplicate_effective_date(tmp_path):
    mw_file = tmp_path / "min_wage.csv"
    events_file = tmp_path / "events.csv"

    mw_data = (
        "sector,effective_date,amount_egp,confidence\n"
        "gov,2020-01-01,2000,high\n"
        "gov,2020-01-01,2500,high\n"
    )
    mw_file.write_text(mw_data, encoding="utf-8")
    events_file.write_text(VALID_EVENTS_CSV, encoding="utf-8")

    with pytest.raises(ValueError, match="Duplicate effective dates found"):
        validate_reference_tables(min_wage_path=mw_file, events_path=events_file)


def test_validate_reference_tables_event_out_of_bounds(tmp_path):
    mw_file = tmp_path / "min_wage.csv"
    events_file = tmp_path / "events.csv"

    mw_data = "sector,effective_date,amount_egp,confidence\ngov,2020-01-01,2000,high\n"
    mw_file.write_text(mw_data, encoding="utf-8")

    events_data = (
        "event_id,event_date,month,type,description,fx_before_egp_per_usd,fx_after_egp_per_usd,"
        "policy_rate_change_bp,source_1,source_2,confidence,note\n"
        "E01,1990-01-01,1990-01,rate,test,30,30,100,src1,,high,test\n"
    )
    events_file.write_text(events_data, encoding="utf-8")

    with pytest.raises(ValueError, match="Events found outside the allowed period"):
        validate_reference_tables(min_wage_path=mw_file, events_path=events_file)