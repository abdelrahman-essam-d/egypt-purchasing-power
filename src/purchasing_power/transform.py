



def real_value(amount, cpi_from, cpi_to):

    if cpi_from <= 0 or cpi_to <= 0:
        raise ValueError("CPI values must be positive numbers.")

    return amount * (cpi_to / cpi_from)


def to_usd(amount, egp_per_usd):
    if egp_per_usd <= 0:
        raise ValueError("Exchange rate must be a positive number.")

    return amount / egp_per_usd








