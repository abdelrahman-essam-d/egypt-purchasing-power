
from pathlib import Path

from purchasing_power.transform import build_monthly_min_wage

if __name__ == "__main__":

    print("Building monthly minimum wage series...")

    df = build_monthly_min_wage()

    output_path = Path("data/processed/min_wage_monthly.csv")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"Saved successfully to: {output_path}")
    print(df.head(10))
    print(df.tail(10))
    print(f"Total months: {len(df)}")
