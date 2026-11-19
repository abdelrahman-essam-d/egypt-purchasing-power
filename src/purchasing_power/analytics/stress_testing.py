





def apply_shocks(
    wage: float,
    cpi: float,
    exchange_rate: float,
    fx_shock_pct: float = 0.0,
    inflation_shock_pct: float = 0.0,
    wage_growth_pct: float = 0.0,
) -> dict:
    """
    Apply hypothetical economic shocks.

    Percentages are expressed as percentage points:
    10 means 10%, not 0.10.
    """

    if wage <= 0 or cpi <= 0 or exchange_rate <= 0:
        raise ValueError("Wage, CPI, and exchange rate must be positive.")

    new_wage = wage * (1 + wage_growth_pct / 100)
    new_cpi = cpi * (1 + inflation_shock_pct / 100)
    new_exchange_rate = exchange_rate * (1 + fx_shock_pct / 100)

    return {
        "new_wage": new_wage,
        "new_cpi": new_cpi,
        "new_exchange_rate": new_exchange_rate,
    }


def calculate_real_wage(
    wage: float,
    cpi: float,
    base_cpi: float = 66.4,
) -> float:

    if wage <= 0 or cpi <= 0 or base_cpi <= 0:
        raise ValueError("Wage and CPI values must be positive.")

    return wage * base_cpi / cpi



def calculate_stress_impact(
    current_real_wage: float,
    new_real_wage: float,
) -> float:

    if current_real_wage <= 0 or new_real_wage < 0:
        raise ValueError("Real wages must be valid positive values.")

    return (
        (new_real_wage - current_real_wage)
        / current_real_wage
    ) * 100




def run_stress_scenario(
    wage: float,
    cpi: float,
    exchange_rate: float,
    fx_shock_pct: float = 0.0,
    inflation_shock_pct: float = 0.0,
    wage_growth_pct: float = 0.0,
    base_cpi: float = 66.4,
) -> dict:

    # Calculate current real wage
    current_real_wage = calculate_real_wage(
        wage=wage,
        cpi=cpi,
        base_cpi=base_cpi,
    )

    # Apply economic shocks
    shocked_values = apply_shocks(
        wage=wage,
        cpi=cpi,
        exchange_rate=exchange_rate,
        fx_shock_pct=fx_shock_pct,
        inflation_shock_pct=inflation_shock_pct,
        wage_growth_pct=wage_growth_pct,
    )

    # Calculate new real wage
    new_real_wage = calculate_real_wage(
        wage=shocked_values["new_wage"],
        cpi=shocked_values["new_cpi"],
        base_cpi=base_cpi,
    )

    # Calculate purchasing power impact
    impact_pct = calculate_stress_impact(
        current_real_wage=current_real_wage,
        new_real_wage=new_real_wage,
    )

    # Calculate real wage in USD
    current_real_wage_usd = current_real_wage / exchange_rate
    new_real_wage_usd = (
        new_real_wage / shocked_values["new_exchange_rate"]
    )

    return {
        "current_real_wage": current_real_wage,
        "new_real_wage": new_real_wage,
        "impact_pct": impact_pct,
        "current_real_wage_usd": current_real_wage_usd,
        "new_real_wage_usd": new_real_wage_usd,
        **shocked_values,
    }
