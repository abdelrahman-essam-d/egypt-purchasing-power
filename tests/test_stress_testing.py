
import pytest

from purchasing_power.analytics.stress_testing import (
    apply_shocks,
    calculate_real_wage,
    calculate_stress_impact,
    run_stress_scenario,
)


def test_apply_shocks():
    result = apply_shocks(
        wage=8000,
        cpi=294.5,
        exchange_rate=52.039,
        fx_shock_pct=10,
        inflation_shock_pct=5,
        wage_growth_pct=0,
    )

    assert result["new_wage"] == 8000
    assert result["new_cpi"] == pytest.approx(309.225)
    assert result["new_exchange_rate"] == pytest.approx(57.2429)


def test_apply_shocks_rejects_non_positive_inputs():
    with pytest.raises(ValueError):
        apply_shocks(
            wage=0,
            cpi=294.5,
            exchange_rate=52.039,
        )

def test_calculate_real_wage():
    result = calculate_real_wage(
        wage=8000,
        cpi=309.225,
    )

    assert result == pytest.approx(1718.45, abs=1)



def test_calculate_stress_impact():
    result = calculate_stress_impact(
        current_real_wage=1800,
        new_real_wage=1718.45,
    )

    assert result == pytest.approx(-4.5306, abs=0.01)



def test_run_stress_scenario():
    result = run_stress_scenario(
        wage=8000,
        cpi=294.5,
        exchange_rate=52.039,
        fx_shock_pct=10,
        inflation_shock_pct=5,
    )
    assert result["new_wage"] == 8000
    assert result["new_cpi"] == pytest.approx(309.225)
    assert result["impact_pct"] == pytest.approx(-4.77, abs=0.1)
    assert result["new_real_wage_usd"] < result["current_real_wage_usd"]




def test_fx_shock_does_not_change_real_wage_egp():
    baseline = run_stress_scenario(
        wage=8000,
        cpi=294.5,
        exchange_rate=52.039,
    )

    shocked = run_stress_scenario(
        wage=8000,
        cpi=294.5,
        exchange_rate=52.039,
        fx_shock_pct=10,
    )

    assert shocked["new_real_wage"] == pytest.approx(
        baseline["new_real_wage"]
    )


def test_fx_shock_changes_real_wage_usd():
    baseline = run_stress_scenario(
        wage=8000,
        cpi=294.5,
        exchange_rate=52.039,
    )

    shocked = run_stress_scenario(
        wage=8000,
        cpi=294.5,
        exchange_rate=52.039,
        fx_shock_pct=10,
    )

    assert shocked["new_real_wage_usd"] < baseline["current_real_wage_usd"]


def test_equal_wage_and_inflation_growth_preserve_real_wage():
    result = run_stress_scenario(
        wage=8000,
        cpi=294.5,
        exchange_rate=52.039,
        inflation_shock_pct=10,
        wage_growth_pct=10,
    )

    assert result["impact_pct"] == pytest.approx(0, abs=1e-9)
