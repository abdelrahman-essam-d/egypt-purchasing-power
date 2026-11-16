import pandas as pd


def summarize_real_wages(df):
    """
    Summarize nominal and real minimum wage changes
    for each sector over its available period.
    """

    df = df.copy()
    df["month"] = pd.PeriodIndex(df["month"], freq="M")
    df = df.sort_values("month")

    sectors = {
        "government": {
            "nominal": "government",
            "real": "government_real",
            "usd": "government_real_usd",
        },
        "private": {
            "nominal": "private",
            "real": "private_real",
            "usd": "private_real_usd",
        },
    }

    results = []

    for sector, columns in sectors.items():

        # Keep only months where nominal and real wages are available
        sector_df = df.dropna(
            subset=[columns["nominal"], columns["real"]]
        )

        if sector_df.empty:
            continue

        first = sector_df.iloc[0]
        last = sector_df.iloc[-1]

        def percentage_change(start_value, end_value):
            if start_value == 0:
                return None

            return (end_value - start_value) / start_value * 100

        results.append({
            "sector": sector,
            "start_month": str(first["month"]),
            "end_month": str(last["month"]),

            "nominal_start": first[columns["nominal"]],
            "nominal_end": last[columns["nominal"]],
            "nominal_change_pct": percentage_change(
                first[columns["nominal"]],
                last[columns["nominal"]]
            ),

            "real_start": first[columns["real"]],
            "real_end": last[columns["real"]],
            "real_change_pct": percentage_change(
                first[columns["real"]],
                last[columns["real"]]
            ),

            "real_usd_start": first[columns["usd"]],
            "real_usd_end": last[columns["usd"]],
            "real_usd_change_pct": percentage_change(
                first[columns["usd"]],
                last[columns["usd"]]
            ),
        })

    return pd.DataFrame(results)






def calculate_recovery(
    df,
    events_path="data/reference/events.csv",
):
    """
    Calculate how many months each wage sector needs
    to recover its real wage level before each event.

    Recovery occurs when real wage >= the pre event baseline.
    """

    df = df.copy()
    events = pd.read_csv(events_path)

    df["month"] = pd.PeriodIndex(df["month"], freq="M")
    events["event_month"] = pd.PeriodIndex(
        events["month"], freq="M"
    )

    df = df.sort_values("month")
    max_month = df["month"].max()

    sectors = {
        "government": "government_real",
        "private": "private_real",
    }

    results = []

    for _, event in events.iterrows():  # iterrows() output is tuple consists of index of the roe and its values

        event_month = event["event_month"]
        baseline_month = event_month - 1

        for sector, real_col in sectors.items():

            baseline_data = df.loc[
                df["month"] == baseline_month,
                real_col
            ]

            # No baseline means recovery cannot be measured
            if baseline_data.empty or pd.isna(baseline_data.iloc[0]):

                results.append({
                    "event_id": event["event_id"],
                    "event_month": str(event_month),
                    "sector": sector,
                    "baseline_month": str(baseline_month),
                    "baseline_real_wage": None,
                    "recovery_month": None,
                    "months_to_recover": None,
                    "status": "no_baseline",
                })

                continue

            baseline_wage = baseline_data.iloc[0]

            # Search from event month onward
            post_event = df[
                (df["month"] >= event_month)
                & (df["month"] <= max_month)
            ]

            recovered = post_event[
                post_event[real_col] >= baseline_wage
            ]

            if recovered.empty:

                recovery_month = None
                months_to_recover = None
                status = "not_recovered"

            else:

                recovery_month = recovered.iloc[0]["month"]

                months_to_recover = (
                    recovery_month - baseline_month
                ).n

                status = "recovered"

            results.append({
                "event_id": event["event_id"],
                "event_month": str(event_month),
                "sector": sector,
                "baseline_month": str(baseline_month),
                "baseline_real_wage": baseline_wage,
                "recovery_month": (
                    str(recovery_month)
                    if recovery_month is not None
                    else None
                ),
                "months_to_recover": months_to_recover,
                "status": status,
            })

    return pd.DataFrame(results)



def compare_2017_wage_sensitivity(
    df,
    min_wage_path="data/reference/min_wage.csv",
    events_path="data/reference/events.csv",
):
    """
    Compare E1 recovery with and without the disputed
    low-confidence government wage of EGP 1,400 in 2017.
    """

    df = df.copy()
    df["month"] = pd.PeriodIndex(df["month"], freq="M")

    # Load reference wage records
    wages = pd.read_csv(min_wage_path)
    wages["effective_date"] = pd.to_datetime(
        wages["effective_date"]
    )

    government = wages[
        wages["sector"] == "government"
    ].sort_values("effective_date").copy()

    # Locate the disputed low-confidence record
    disputed = government[
        (government["confidence"] == "low")
        & (government["amount_egp"] == 1400)
    ]

    if len(disputed) != 1:
        raise ValueError(
            "Expected exactly one disputed government wage "
            "record of EGP 1,400 with low confidence."
        )

    disputed = disputed.iloc[0]
    disputed_month = disputed["effective_date"].to_period("M")

    # Find the wage immediately before the disputed record
    previous_records = government[
        government["effective_date"] < disputed["effective_date"]
    ]

    if previous_records.empty:
        raise ValueError("Previous government wage not found.")

    previous_wage = previous_records.iloc[-1]["amount_egp"]

    # Find the next government wage after the disputed record
    next_records = government[
        government["effective_date"] > disputed["effective_date"]
    ]

    if next_records.empty:
        raise ValueError("Next government wage not found.")

    next_month = next_records.iloc[0]["effective_date"].to_period("M")

    # Scenario 1: Keep the original data (with EGP 1,400)
    with_1400 = df.copy()

    # Scenario 2: Remove the disputed increase
    without_1400 = df.copy()

    mask = (
        (without_1400["month"] >= disputed_month)
        & (without_1400["month"] < next_month)
    )

    without_1400.loc[mask, "government"] = previous_wage

    # Recalculate real government wages in the alternative scenario
    base_month = without_1400["month"].min()

    base_cpi = without_1400.loc[
        without_1400["month"] == base_month,
        "cpi_index"
    ].iloc[0]

    without_1400["government_real"] = (
        without_1400["government"] * base_cpi
        / without_1400["cpi_index"]
    )

    # Calculate recovery in both scenarios
    results = []

    for scenario, scenario_df in [
        ("with_1400", with_1400),
        ("without_1400", without_1400),
    ]:

        recovery = calculate_recovery(
            scenario_df,
            events_path=events_path,
        )

        e1_government = recovery[
            (recovery["event_id"] == "E1")
            & (recovery["sector"] == "government")
        ].iloc[0]

        results.append({
            "scenario": scenario,
            "baseline_real_wage": e1_government[
                "baseline_real_wage"
            ],
            "recovery_month": e1_government["recovery_month"],
            "months_to_recover": e1_government[
                "months_to_recover"
            ],
            "status": e1_government["status"],
        })

    return pd.DataFrame(results)