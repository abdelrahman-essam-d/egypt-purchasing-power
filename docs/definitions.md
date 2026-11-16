# Economic Definitions and Methodology

## 1. Real Minimum Wage

Real minimum wage measures the purchasing power of nominal wages after adjusting for inflation.

\[
RealWage_t = NominalWage_t \times \frac{CPI_{base}}{CPI_t}
\]

- Base month: October 2016.
- All real EGP wages are expressed in October 2016 purchasing power.
- CPI is the monthly consumer price index.

## 2. Real Wage Converted to USD

\[
RealWageUSD_t = \frac{RealWageEGP_t}{OfficialFX_t}
\]

This indicator converts the real EGP wage using the contemporaneous official exchange rate. It is not a constant-purchasing-power USD measure.

## 3. Recovery Analysis

For each economic event:

- Baseline month: the month immediately preceding the event.
- Baseline wage: real wage in the baseline month.
- Recovery month: the first month from the event month onward in which real wage equals or exceeds the baseline.
- Months to recover: calendar-month difference between the recovery month and baseline month.
- Not recovered: baseline exists, but recovery was not observed by the end of the dataset.
- No baseline: insufficient wage data before the event.

Recovery is an observed threshold crossing, not proof that the event caused the wage movement.

## 4. Sensitivity Analysis

The disputed government minimum wage of EGP 1,400 in July 2017 is tested under two scenarios:

- With EGP 1,400.
- Without EGP 1,400, retaining EGP 1,200 until the next documented wage change.

Both scenarios produce the same E1 recovery month: July 2019 (33 months).

## 5. Data Limitations

- Monthly observations cannot identify within-month changes.
- The private-sector wage series starts in January 2022.
- Wage-source confidence varies across reference records.
- Only six selected economic events are analyzed.
- Recovery does not establish causation.
- The USD-converted indicator uses the official nominal exchange rate.