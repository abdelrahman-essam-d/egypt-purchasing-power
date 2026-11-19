# ADR 0006: Forecasting Protocol

- **Status:** Accepted
- **Date:** 2026-11-19

## 1. Objective

Evaluate whether forecasting models can predict Egyptian monthly inflation more accurately than simple baseline models.

The goal is economic intelligence, not merely model accuracy.

## 2. Target Variable

Target: `cpi_mom_pct`

Formula:

\[
CPI_{MoM} = \left(\frac{CPI_t}{CPI_{t-1}}-1\right)\times 100
\]

The target represents the monthly percentage change in Egypt's CPI.

## 3. Forecast Horizons

- 1 month ahead.
- 3 months ahead.

Each horizon will be evaluated separately.

## 4. Models

### Baseline models
1. Naive: predicts the latest observed CPI monthly change.
2. Drift: extrapolates the average historical trend.

### Statistical model
3. ETS: Exponential Smoothing model.

### Machine Learning model
4. Ridge Regression using lagged economic indicators.

All models must use past information only.

## 5. Evaluation Strategy

Use expanding-window rolling-origin evaluation.

- Initial training window: 48 monthly observations.
- Evaluation target months: March 2026 through September 2026.
- Forecast horizons: 1 and 3 months.
- Training data at each origin must not include observations after that origin.
- Model specifications and hyperparameters must be fixed before evaluating the holdout period.
- Actual observations may enter subsequent training windows as they become available.

For a 3-month horizon, the forecast origin must be three months before the target month.

## 6. Evaluation Metrics

### MAE

Mean Absolute Error:

\[
MAE = \frac{1}{n}\sum_{i=1}^{n}|y_i-\hat{y}_i|
\]

### MASE

Mean Absolute Scaled Error.

MASE will compare forecasting errors against the in-sample one-step naive benchmark.

Interpretation:
- MASE below 1: better than the naive benchmark.
- MASE equal to 1: equivalent to the benchmark.
- MASE above 1: worse than the benchmark.

## 7. Data Leakage Prevention

- No future observations in training features.
- All lagged features must be constructed using past observations only.
- Preprocessing and scaling must be fitted on training data only.
- Hyperparameters must not be tuned using the evaluation period.
- Each forecast must be reproducible from its forecast origin.

## 8. Limitations

- The available dataset contains approximately 120 monthly observations.
- The evaluation period is short.
- Results are descriptive and do not establish economic causality.
- Model performance may change during structural economic breaks.
- Forecasts should not be interpreted as guaranteed future outcomes.

## 9. Decision Rule

A complex model will only be considered useful if it demonstrates better out-of-sample performance than the naive baseline.

If the naive model performs best, that result will be reported honestly.