

import pandas as pd

from purchasing_power.analysis import (
    compare_2017_wage_sensitivity,
)

if __name__ == "__main__":

    print("Starting sensitivity analysis...")

    df = pd.read_csv(
        "data/processed/real_min_wage_monthly.csv"
    )

    results = compare_2017_wage_sensitivity(df)

    print("\nE1 Sensitivity Analysis:")
    print(results.to_string(index=False))

    results.to_csv(
        "data/processed/e1_sensitivity.csv",
        index=False,
    )

    print("\nSensitivity analysis completed!")