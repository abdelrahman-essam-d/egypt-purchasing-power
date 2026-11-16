
import duckdb
import pytest


def test_monthly_fx_change_sql():

    conn = duckdb.connect(":memory:")

    conn.execute("""
        CREATE TABLE economic_indicators (
            month VARCHAR,
            egp_per_usd DOUBLE
        )
    """)

    conn.execute("""
        INSERT INTO economic_indicators VALUES
        ('2024-01', 30.0),
        ('2024-02', 33.0),
        ('2024-03', 36.0)
    """)

    result = conn.execute("""
        SELECT
            month,
            egp_per_usd,

            LAG(egp_per_usd) OVER (
                ORDER BY month
            ) AS previous_fx,

            (
                egp_per_usd /
                LAG(egp_per_usd) OVER (
                    ORDER BY month
                ) - 1
            ) * 100 AS fx_change_pct

        FROM economic_indicators

        ORDER BY month
    """).fetchdf()

    assert result.loc[0, "previous_fx"] is None or \
        result.loc[0, "previous_fx"] != result.loc[0, "previous_fx"]

    assert result.loc[1, "fx_change_pct"] == pytest.approx(10.0)
    assert result.loc[2, "fx_change_pct"] == pytest.approx(100 / 11)

    conn.close()


def test_running_maximum_sql():

    conn = duckdb.connect(":memory:")

    conn.execute("""
        CREATE TABLE real_wages (
            month VARCHAR,
            government_real DOUBLE
        )
    """)

    conn.execute("""
        INSERT INTO real_wages VALUES
        ('2024-01', 1000),
        ('2024-02', 900),
        ('2024-03', 1100)
    """)

    result = conn.execute("""
        SELECT
            month,
            government_real,

            MAX(government_real) OVER (
                ORDER BY month
            ) AS government_max

        FROM real_wages

        ORDER BY month
    """).fetchdf()

    assert result["government_max"].tolist() == [
        1000, 1000, 1100
    ]

    conn.close()
