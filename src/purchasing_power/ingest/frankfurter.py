from pathlib import Path

import pandas as pd
import requests


def fetch_data(
    start_date="2000-01-01",
    end_date="2026-03-31",
    quote="EGP",
    base="USD",
):

    url = "https://api.frankfurter.dev/v2/rates"

    # 4 keys
    params = {
        "from": start_date,
        "to": end_date,
        "base": base,
        "quotes": quote,
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()


def save_data_csv(data, file_path):

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(data)
    df.to_csv(path, index=False, encoding="utf-8-sig")

    print(f"Saved successfully in {path}")

    return path
