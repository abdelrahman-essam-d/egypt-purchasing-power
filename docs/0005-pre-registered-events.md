# 0005 - Write the event list before running any anomaly model

- **Status:** Accepted
- **Date:** 2026-11-15

## Context

Anomaly detection has no labels. If the list of "real" events is written after looking at the model output, it is easy (and unintentional) to pick events the model already found. With only six events, one such choice changes the result.

## Decision

- `data/reference/events.csv` is created and **committed before** any anomaly model is run. The commit date is the proof.
- The list is fixed: E1 Nov 2016 float, E2 Mar 2022, E3 Oct 2022, E4 Jan 2023, E5 Mar 2024, E6 Mar 2026. Every event has two sources and a confidence level.
- `type` separates official policy moves (`official_float`, `official_devaluation`, `official_depreciation`) from market moves (`market_depreciation`, E6). Results are reported with and without E6.
- An event counts as detected if the model flags the event month or one month either side. False alarms are counted separately.
- Isolation Forest is compared with a rolling robust z-score (median and MAD) on rates of change, not on levels.
- Events are not added or removed after the first model run. A new event goes in a new list with a new commit.

## Consequences

- Six events is too few to say one method is better. The README reports hits, misses and false alarms as a description only.
- Rate levels are not stored (sources disagree). Only the size of the policy-rate change is kept, and it is empty when the source does not report it.
- Same logic for forecasting: the test protocol (ADR 0006, to write) is committed before running the models.
