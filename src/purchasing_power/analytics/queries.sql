
-- Query 1: monthly changes in FX and CPI

WITH monthly_data AS (

    SELECT             -- LAG() is a SQL window function that accesses data from 
        month,         -- a previous row in the same result set without using a self-join.
        egp_per_usd,
        cpi_index,

        LAG(egp_per_usd) OVER (
            ORDER BY month
        ) AS previous_fx,

        LAG(cpi_index) OVER (
            ORDER BY month
        ) AS previous_cpi

    FROM economic_indicators

)

SELECT
    month,
    egp_per_usd,
    previous_fx,

    egp_per_usd - previous_fx AS fx_change,

    (egp_per_usd / previous_fx - 1) * 100
        AS fx_change_pct,

    cpi_index,
    previous_cpi,

    (cpi_index / previous_cpi - 1) * 100
        AS cpi_change_pct

FROM monthly_data

ORDER BY month;





-- Query 2: Real wages compared to previous maximum

SELECT
    month,

    government_real,

    MAX(government_real) OVER (
        ORDER BY month
    ) AS government_max,

    government_real -
    MAX(government_real) OVER (
        ORDER BY month
    ) AS government_gap,

    private_real,

    MAX(private_real) OVER (
        ORDER BY month
    ) AS private_max,

    private_real -
    MAX(private_real) OVER (
        ORDER BY month
    ) AS private_gap

FROM real_wages

ORDER BY month;




-- Query 3: Top 10 implied FX gaps

SELECT
    month,
    egp_per_usd,
    implied_egp_per_usd,
    implied_fx_gap_pct

FROM implied_fx

ORDER BY implied_fx_gap_pct DESC

LIMIT 10;





-- Query 4: Compare real wages between sectors

SELECT
    w.month,

    w.government_real,
    w.private_real,

    w.government_real - w.private_real
        AS wage_difference

FROM real_wages AS w

INNER JOIN economic_indicators AS e
    ON w.month = e.month

WHERE w.private_real IS NOT NULL

ORDER BY w.month;




-- Query 5: Recovery analysis by economic event

SELECT
    r.event_id,
    e.event_date,
    e.type,
    e.description,

    r.sector,
    r.baseline_month,
    r.recovery_month,
    r.months_to_recover,

    CASE                            -- CASE WHEN Executing conditions and choosing a result based on them
        WHEN r.status = 'recovered'
            THEN 'Recovered'

        WHEN r.status = 'not_recovered'
            THEN 'Not Recovered'

        ELSE 'No Baseline'
    END AS recovery_status

FROM wage_recovery AS r

INNER JOIN events AS e
    ON r.event_id = e.event_id

ORDER BY
    e.event_date,
    r.sector;
