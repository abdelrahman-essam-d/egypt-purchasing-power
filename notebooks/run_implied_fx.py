



from pathlib import Path

import pandas as pd

from purchasing_power.analysis import calculate_implied_fx

if __name__ == "__main__":

    print("Starting implied exchange rate analysis...")

    input_path = Path(
        "data/processed/economic_indicators_monthly.csv"
    )

    df = pd.read_csv(input_path)

    df = calculate_implied_fx(df)

    output_path = Path(
        "data/processed/implied_fx_monthly.csv"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print("\nImplied FX Analysis:")
    print(
        df[
            [
                "month",
                "egp_per_usd",
                "implied_egp_per_usd",
                "implied_fx_gap_pct",
            ]
        ].head(10).to_string(index=False)
    )

    print("\nLast 10 months:")
    print(
        df[
            [
                "month",
                "egp_per_usd",
                "implied_egp_per_usd",
                "implied_fx_gap_pct",
            ]
        ].tail(10).to_string(index=False)
    )

    print("\nTotal months:", len(df))
    print("Analysis completed successfully!")
