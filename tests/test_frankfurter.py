import pandas as pd
import pytest
import requests

from purchasing_power.ingest.frankfurter import fetch_data, save_data_csv


def test_fetch_data_success(mocker):

    mock_response = mocker.Mock()

    mock_response.json.return_value = [
        {"date": "2026-01-01", "base": "USD", "quote": "EGP", "rate": 47.5}
    ]

    mocker.patch(  # dont send real request, and send our mock req.
        "purchasing_power.ingest.frankfurter.requests.get", return_value=mock_response
    )

    result = fetch_data(start_date="2026-01-01", end_date="2026-01-31", quote="EGP", base="USD")

    assert len(result) == 1
    assert result[0]["rate"] == 47.5


def test_fetch_data_http_error(mocker):

    mock_response = mocker.Mock()

    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Client Error: Not Found"
    )

    mocker.patch("purchasing_power.ingest.frankfurter.requests.get", return_value=mock_response)

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_data(start_date="2026-01-01", end_date="2026-01-31", quote="EGP", base="USD")


def test_save_data_csv(mocker, tmp_path):

    data = [{"date": "2026-01-01", "rate": 47.5}, {"date": "2026-01-02", "rate": 47.6}]

    file_path = tmp_path / "raw" / "frankfurter.csv"

    result = save_data_csv(data, file_path)

    assert result.exists()

    df = pd.read_csv(result)

    assert len(df) == 2
    assert df.loc[0, "rate"] == 47.5
