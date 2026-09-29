"""Pricing and revenue scenario analysis for the ThaiBev commercial analytics case study.

This script creates a simple sensitivity model that translates price-change and
demand-elasticity assumptions into expected revenue impact. It is intentionally
scenario-based because the public dataset does not include ThaiBev transaction-level
prices, units, margins, or customer/channel mix.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parent
BEER_SALES_FILE = PROJECT_ROOT / "beer_sales_monthly.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

PRICE_CHANGES = [-0.02, 0.00, 0.01, 0.03, 0.05, 0.08]
ELASTICITIES = [-1.50, -1.20, -1.00, -0.70, -0.30]


def build_scenario_table() -> pd.DataFrame:
    """Return pricing sensitivity table using public beer-sales value as market proxy."""
    beer_sales = pd.read_csv(BEER_SALES_FILE)
    beer_sales["date"] = pd.to_datetime(beer_sales["date"], format="%m/%Y")
    beer_sales["sale"] = pd.to_numeric(beer_sales["sale"], errors="raise")

    recent_12m_sales = beer_sales.tail(12)["sale"].sum()
    rows = []
    for price_change in PRICE_CHANGES:
        for elasticity in ELASTICITIES:
            volume_change = elasticity * price_change
            revenue_multiplier = (1 + price_change) * (1 + volume_change)
            revenue_impact_pct = revenue_multiplier - 1
            revenue_impact_thb = recent_12m_sales * revenue_impact_pct
            rows.append(
                {
                    "price_change_pct": price_change * 100,
                    "elasticity": elasticity,
                    "estimated_volume_change_pct": volume_change * 100,
                    "estimated_revenue_impact_pct": revenue_impact_pct * 100,
                    "estimated_revenue_impact_thb": revenue_impact_thb,
                }
            )
    return pd.DataFrame(rows)


def write_outputs(scenario_df: pd.DataFrame) -> None:
    scenario_df.to_csv(OUTPUT_DIR / "pricing_revenue_sensitivity.csv", index=False)

    heatmap_data = scenario_df.pivot(
        index="elasticity",
        columns="price_change_pct",
        values="estimated_revenue_impact_pct",
    ).sort_index(ascending=False)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        center=0,
        linewidths=0.5,
        cbar_kws={"label": "Estimated revenue impact (%)"},
        ax=ax,
    )
    ax.set_title(
        "ThaiBev Pricing Sensitivity: Revenue Impact by Price Change and Demand Elasticity",
        fontsize=12,
        fontweight="bold",
    )
    ax.set_xlabel("Price change (%)")
    ax.set_ylabel("Demand elasticity assumption")
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "pricing_revenue_heatmap.png", dpi=180)


def main() -> None:
    scenario_df = build_scenario_table()
    write_outputs(scenario_df)

    print("Pricing scenario outputs written:")
    print(f"- {OUTPUT_DIR / 'pricing_revenue_sensitivity.csv'}")
    print(f"- {OUTPUT_DIR / 'pricing_revenue_heatmap.png'}")
    print("\nSample scenarios:")
    print(
        scenario_df[
            (scenario_df["price_change_pct"].isin([1.0, 3.0, 5.0]))
            & (scenario_df["elasticity"].isin([-1.2, -0.7, -0.3]))
        ].to_string(index=False)
    )


if __name__ == "__main__":
    main()
