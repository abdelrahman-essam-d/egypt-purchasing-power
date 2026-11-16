

import pandas as pd

from purchasing_power.analysis import calculate_recovery


def create_test_data(government_values, private_values):
    months = pd.period_range("2020-01", periods=5, freq="M")

    return pd.DataFrame({
        "month": months,
        "government_real": government_values,
        "private_real": private_values,
    })


def create_event_file(tmp_path):
    events = pd.DataFrame({
        "event_id": ["E1"],
        "month": ["2020-02"],
    })

    path = tmp_path / "events.csv"
    events.to_csv(path, index=False)

    return path


def test_recovery_after_two_months(tmp_path):

    df = create_test_data(
        government_values=[100, 70, 80, 110, 120],
        private_values=[100, 70, 80, 110, 120],
    )

    events_path = create_event_file(tmp_path)

    result = calculate_recovery(df, events_path)

    government = result[result["sector"] == "government"].iloc[0]

    assert government["status"] == "recovered"
    assert government["recovery_month"] == "2020-04"
    assert government["months_to_recover"] == 3


def test_not_recovered(tmp_path):

    df = create_test_data(
        government_values=[100, 70, 80, 90, 95],
        private_values=[100, 70, 80, 90, 95],
    )

    events_path = create_event_file(tmp_path)

    result = calculate_recovery(df, events_path)

    government = result[result["sector"] == "government"].iloc[0]

    assert government["status"] == "not_recovered"
    assert pd.isna(government["recovery_month"])
    assert pd.isna(government["months_to_recover"])


def test_recovery_in_event_month(tmp_path):

    df = create_test_data(
        government_values=[100, 110, 120, 130, 140],
        private_values=[100, 110, 120, 130, 140],
    )

    events_path = create_event_file(tmp_path)

    result = calculate_recovery(df, events_path)

    government = result[result["sector"] == "government"].iloc[0]

    assert government["status"] == "recovered"
    assert government["recovery_month"] == "2020-02"
    assert government["months_to_recover"] == 1
