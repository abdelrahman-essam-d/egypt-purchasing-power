from pathlib import Path

import pandas as pd

from purchasing_power.analysis import summarize_real_wages

if __name__ == "__main__":

    print("Starting real wage summary analysis...")

    # 1. Load real wage dataset
    input_path = Path("data/processed/real_min_wage_monthly.csv")
    df = pd.read_csv(input_path)

    # 2. Calculate summary
    summary = summarize_real_wages(df)

    # 3. Save summary
    output_path = Path("data/processed/real_wage_summary.csv")
    summary.to_csv(output_path, index=False)

    # 4. Display results
    print("\nReal Wage Summary:")
    print(summary.to_string(index=False))

    print("\nAnalysis completed successfully!")