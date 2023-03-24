import numpy as np

from config import production_tax, production_value, exchange_fuzzy_probability


def perform_exchange(
    wealth_1: float,
    wealth_2: float,
):
    production = production_value * (1 - production_tax)
    total_fuzzy = (
        wealth_1**exchange_fuzzy_probability + wealth_2**exchange_fuzzy_probability
    )
    new_wealth_1 = (
        (wealth_1**exchange_fuzzy_probability) * production / total_fuzzy
        if wealth_1 > 0
        else wealth_1
    )
    new_wealth_2 = (
        (wealth_2**exchange_fuzzy_probability) * production / total_fuzzy
        if wealth_2 > 0
        else wealth_2
    )

    return new_wealth_1, new_wealth_2


def expected_exchange(
    wealth_1: np.array,
    state_avg_wealth: np.array,
    probability_array: np.array,
    people_by_state_array: np.array,
) -> np.array:
    # calculate production
    production = production_value * (wealth_1 + state_avg_wealth)
    # takes out gov part
    production_tax_gov = production_tax * production
    production = production - production_tax_gov
    # puts a minimal value to not make a division by zero
    wealth_1[wealth_1 == 0] = 0.01
    # separates it to exchange_gain
    total_fuzzy = (
        wealth_1**exchange_fuzzy_probability
        + state_avg_wealth**exchange_fuzzy_probability
    )
    exchange_gain = (wealth_1**exchange_fuzzy_probability) / total_fuzzy * production
    # treats any nan case to zero
    exchange_gain = np.nan_to_num(exchange_gain, copy=True, nan=0.0)

    exchange_gain = (
        (wealth_1**exchange_fuzzy_probability)
        * people_by_state_array
        / probability_array
    )
    return exchange_gain
