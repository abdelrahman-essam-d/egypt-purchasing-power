
from pathlib import Path

from purchasing_power.transform import (
    calculate_real_wage,
    calculate_real_wage_usd,
    merge_wage_economic_data,
)

if __name__ == "__main__":

    print("Starting real wage analysis...")

    # 1. Merge datasets
    df = merge_wage_economic_data()

    # 2. Calculate government real wage
    df = calculate_real_wage(
        df,
        wage_col="government"
    )

    df = calculate_real_wage_usd(
        df,
        real_wage_col="government_real"
    )

    # 3. Calculate private real wage
    df = calculate_real_wage(
        df,
        wage_col="private"
    )

    df = calculate_real_wage_usd(
        df,
        real_wage_col="private_real"
    )

    # 4. Save results
    output_path = Path("data/processed/real_min_wage_monthly.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print("Real wage analysis completed successfully!")
    print(df.head())
    print(df.tail())
    print(f"Total months: {len(df)}")
