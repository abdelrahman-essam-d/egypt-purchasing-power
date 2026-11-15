# 0004 - Minimum wage: two series, with a confidence level per row

- **Status:** Accepted
- **Date:** 2026-11-15

## Context

There is no single official minimum wage table for the whole window. The government minimum wage exists from before 2016. The private-sector minimum wage started on 1 January 2022. Sources are news articles, and some disagree.

## Decision

- `data/reference/min_wage.csv` has one row per change, with `sector` (`government` or `private`), `amount_egp`, `announce_date`, `effective_date`, two sources, `confidence` (`high`, `medium`, `low`) and a `note`.
- `effective_date` always uses the first day of the month when the source gives only a month.
- **Question 2 (recovery after each float) uses the government series**, because it is the only one that covers 2016-2021. The private series is used from 2022.
- Rows with `confidence = low` are kept, marked, and listed in the README. They are not hidden.

## Open conflicts (stated in the README)

1. **1,400 in July 2017.** Al Arabiya (Sep 2023) says the minimum rose from 1,200 to 1,400 in 2017 and from 1,400 to 2,000 in 2019. Two articles from March 2019 (Egyptian Streets, Enterprise) say the current minimum was 1,200 and call the 2019 raise the first since 2014. The month "July 2017" is an inference (start of the fiscal year), not stated by the source. **Sensitivity:** the November 2016 float starts from 1,200 in both versions, so the baseline does not change. Recovery time is computed twice (with and without the 2017 raise).
2. **2,700: April or July 2022.** Text sources say July 2022. A news-agency infographic says April 2022. The table uses July.
3. **Government 4,000 or 6,000 before July 2025.** Resolved: government 6,000 from March 2024 (three sources). The "previous 4,000" in April 2025 articles is wrong or outdated.

## Consequences

- Every number was read by a summarising tool, so each must be checked against its source before the CSV is trusted.
- Official decrees were not found. Only press coverage supports these rows.
