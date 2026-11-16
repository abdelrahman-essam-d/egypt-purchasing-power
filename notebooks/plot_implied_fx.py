

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(
    "data/processed/implied_fx_monthly.csv"
)

df["month"] = pd.PeriodIndex(df["month"], freq="M").to_timestamp()

output_dir = Path("reports/figures")
output_dir.mkdir(parents=True, exist_ok=True)


# Chart 1: Official vs Implied FX
plt.figure(figsize=(12, 6))

plt.plot(
    df["month"],
    df["egp_per_usd"],
    label="Official FX",
)

plt.plot(
    df["month"],
    df["implied_egp_per_usd"],
    label="Implied FX",
)

plt.title("Official vs Implied Exchange Rate")
plt.xlabel("Month")
plt.ylabel("EGP per USD")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    output_dir / "official_vs_implied_fx.png",
    dpi=150,
)

plt.close()


# Chart 2: Implied FX Gap
plt.figure(figsize=(12, 6))

plt.plot(
    df["month"],
    df["implied_fx_gap_pct"],
    label="Implied FX Gap",
)

plt.axhline(
    y=0,
    linestyle="--",
    label="Zero Gap",
)

plt.title("Implied Exchange Rate Gap")
plt.xlabel("Month")
plt.ylabel("Gap (%)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    output_dir / "implied_fx_gap.png",
    dpi=150,
)

plt.close()

print("Charts generated successfully!")
