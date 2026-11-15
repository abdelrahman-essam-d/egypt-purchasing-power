import pandas as pd
import pytest
from purchasing_power.config import END, START

from purchasing_power.validate import (
    check_missing_or_duplicate_months,
    check_positive_values,
    validate_dataset,
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
