
from pathlib import Path

import pandas as pd

from purchasing_power.analytics.stress_testing import run_stress_scenario


def run_stress_testing():

    print("Starting stress testing...")

    data_path = Path("data/processed/real_min_wage_monthly.csv")
    output_path = Path("data/processed/stress_test_results.csv")

    df = pd.read_csv(data_path)

    # Get the latest available month
    latest_month = df["month"].max()
    latest_data = df.loc[df["month"] == latest_month].iloc[0]

    # Define economic scenarios
    scenarios = {
        "baseline": {
            "fx_shock_pct": 0,
            "inflation_shock_pct": 0,
            "wage_growth_pct": 0,
        },
        "mild": {
            "fx_shock_pct": 5,
            "inflation_shock_pct": 3,
            "wage_growth_pct": 0,
        },
        "moderate": {
            "fx_shock_pct": 10,
            "inflation_shock_pct": 5,
            "wage_growth_pct": 0,
        },
        "severe": {
            "fx_shock_pct": 20,
            "inflation_shock_pct": 10,
            "wage_growth_pct": 0,
        },
        "wage_adjustment": {
            "fx_shock_pct": 10,
            "inflation_shock_pct": 10,
            "wage_growth_pct": 10,
        },
    }

    results = []

    # Apply scenarios to both sectors
    for sector in ["government", "private"]:

        wage = latest_data[sector]

        if pd.isna(wage):
            continue

        for scenario_name, shocks in scenarios.items():

            result = run_stress_scenario(
                wage=wage,
                cpi=latest_data["cpi_index"],
                exchange_rate=latest_data["egp_per_usd"],
                **shocks,
            )

            results.append({
                "month": latest_month,
                "sector": sector,
                "scenario": scenario_name,
                "fx_shock_pct": shocks["fx_shock_pct"],
                "inflation_shock_pct": shocks["inflation_shock_pct"],
                "wage_growth_pct": shocks["wage_growth_pct"],
                **result,
            })

    results_df = pd.DataFrame(results)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_path, index=False)

    print(f"Stress testing completed for {latest_month}!")
    print(f"Results saved to: {output_path}")

    print("\nStress Testing Results:")
    print(
        results_df[
            [
                "sector",
                "scenario",
                "impact_pct",
                "current_real_wage_usd",
                "new_real_wage_usd",
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    run_stress_testing()
