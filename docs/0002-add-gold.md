# 0002 - Add gold prices (world and local)

- **Status:** Accepted
- **Date:** 2026-11-15

## Context

Question 3 asks how far the official EGP/USD rate was from the rate implied by gold:

```
implied_egp_per_usd = local_gold24_egp_per_gram / (world_gold_usd_per_oz / 31.1035)
gap = (implied - official) / official
```

This needs two monthly series from 2016-10: local gold in EGP and world gold in USD.

## Decision

- **World gold:** TradingView `TVC:GOLD`, USD per ounce, **month close**. (The source was first written down as `OANDA:XAUUSD` by mistake; it was corrected to `TVC:GOLD` in all 120 rows.)
- **Local gold:** ayarak.com, **24k**, EGP per gram, **last available day of the month**. The file keeps `obs_date` so the exact day is visible.
- **Why 24k:** 21k = 24k x 0.875, so one karat is enough, and 24k is the base of the implied-rate formula.
- **Window:** starts 2016-10 (see 0003).
- Values were collected by hand and checked with `validate.py` (no missing or duplicate months, first and last month match `config.py`, all values positive).

## Alternatives rejected

| Source | Why rejected |
|---|---|
| goldprice.org | Not usable as the main source for a local EGP series with month-close dates. |
| Amwal Al Ghad (local price) | Wrong value found: 12 Jul 2023 showed 1,686 for 21k, while ayarak and Kaggle show 2,160-2,180. |
| Kaggle gold dataset | 23 values of "3 EGP", a gap from Dec 2024 to Sep 2025, and a duplicated date. Used for one comparison only. |
| `OANDA:XAUUSD` | Wrong source name. The values come from `TVC:GOLD`. |

## Consequences

- The series is hand-collected, so every file needs its `source` column and a validation run.
- ayarak.com and TradingView keep their rights. The raw CSVs are **not** committed (`data/processed/*.csv` is in `.gitignore`). The README explains how to rebuild them.
- Timing mismatch: CPI is a monthly index, while gold and the exchange rate are month-end values. This is a known limitation and is stated in the README.
