

from pathlib import Path

import pandas as pd

from purchasing_power.analysis import calculate_recovery

if __name__ == "__main__":

    print("Starting recovery analysis...")

    input_path = Path(
        "data/processed/real_min_wage_monthly.csv"
    )

    df = pd.read_csv(input_path)

    recovery = calculate_recovery(df)

    output_path = Path(
        "data/processed/wage_recovery.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    recovery.to_csv(output_path, index=False)

    print("\nRecovery Analysis:")
    print(recovery.to_string(index=False))

    print("\nRecovery analysis completed!")
