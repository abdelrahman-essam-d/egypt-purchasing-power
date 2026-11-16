

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":

    df = pd.read_csv("data/processed/real_min_wage_monthly.csv")

    df["month"] = pd.to_datetime(df["month"])

    sectors = {
        "government": "Government",
        "private": "Private",
    }

    output_dir = Path("reports/figures")
    output_dir.mkdir(parents=True, exist_ok=True)

    for sector, title in sectors.items():

        sector_df = df.dropna(
            subset=[sector, f"{sector}_real"]
        ).copy()

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(
            sector_df["month"],
            sector_df[sector],
            label="Nominal Wage (EGP)",
        )

        ax.plot(
            sector_df["month"],
            sector_df[f"{sector}_real"],
            label="Real Wage (2016 EGP)",
        )

        ax.set_title(f"{title} Minimum Wage: Nominal vs Real")
        ax.set_xlabel("Month")
        ax.set_ylabel("Wage (EGP)")
        ax.legend()
        ax.grid(True, alpha=0.3)

        fig.tight_layout()

        fig.savefig(
            output_dir / f"{sector}_nominal_vs_real.png",
            dpi=150,
        )

        plt.close(fig)

    print("Charts generated successfully!")
