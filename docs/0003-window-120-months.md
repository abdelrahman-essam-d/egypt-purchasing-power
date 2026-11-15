# 0003 - Use a 120-month window (2016-10 to 2026-09)

- **Status:** Accepted
- **Date:** 2026-11-15

## Context

The free monthly sources cover about ten years. Longer monthly history (for example 25 years) is paid. The exchange rate regime also changed in November 2016: before it, the pound was a managed peg, which is a different process from the floating rate that came after.

## Decision

- The dataset covers **2016-10 to 2026-09 = 120 months**.
- `START` and `END` live in `src/purchasing_power/config.py`. No code uses the number 120.
- The data month is the first day of the month. Exchange rate and gold are month-end values. The 2026-10 row (25 Oct) was removed because it is outside the window and not a month-end.
- The README states: *"Window: 120 months (Oct 2016 - Sep 2026). Longer free monthly history was not available for all four series. The code takes the window from `config.py`, so extending it is a configuration change, not a rewrite."*

## Alternatives considered

- **Buy longer history.** Rejected: it costs money, and the pre-2016 data comes from a different exchange rate regime, so it would not clearly help forecasting.
- **A shorter window (for example from 2022).** Rejected: it loses the November 2016 float, which is one of the events the project studies.

## Consequences

- 120 points are enough for descriptive analysis. The machine-learning results (forecasting and anomaly detection) are **descriptive, not proof**, and the README says so.
- Extending the window means changing `config.py` and adding data files that pass `validate.py`.
- Planned: a test that runs the pipeline on 240 synthetic months to show the code is not tied to 120.
