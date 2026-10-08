
from purchasing_power.transform import real_value, to_usd


def test_real_value_hand_computed():
    # prices rose 50% (CPI 80 -> 120), so 2000 EGP then = 3000 EGP now
    assert real_value(2000, 80, 120) == 3000


def test_to_usd_hand_computed():
    # 10000 EGP at 50 EGP per USD = 200 USD
    assert to_usd(10000, 50) == 200