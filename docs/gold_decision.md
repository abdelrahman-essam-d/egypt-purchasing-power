# Add Gold 24-karat Local and Global prices as a secondary purchasing power benchmark

Date 2026-10-14

## Context
The project analyzes Egyptian purchasing power and wage values. While official inflation and exchange rates track standard metrics, people in Egypt heavily use gold to save money and protect wealth. To capture this accurately, we track pure 24-karat gold across both international markets and the local Egyptian market.

## Decision
We include 24-karat gold prices in both local and global markets as a secondary benchmark, starting from October 2016 using month-end closing values, sourced from Ayrak. This helps us measure how well wages preserve value relative to a hard asset and allows us to track local market price differences compared to global rates.

## Alternatives we rejected
- Using goldprice.org because it multiplies global prices by the USD rate.
- Using Amwal Al Ghad because the numbers were incorrect.
- Using Kaggle datasets because they contained unrealistic values like 3 pounds and severe data gaps.
- Using mixed karats like 21-karat, since 24-karat provides a clean standard for pure gold.
- Tracking only local or only global prices because we need both to see local market premiums.

## Consequences and risks
- Good: Provides a complete view of asset-based wealth preservation alongside consumer inflation.
- Risk: Local gold prices in Egypt can sometimes disconnect from global prices due to domestic market conditions.
- Mitigation: We track both local and global series side by side to understand these market differences.