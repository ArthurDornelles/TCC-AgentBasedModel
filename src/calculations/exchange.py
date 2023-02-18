import numpy as np

from config import production_tax, production_coefficient, exchange_fuzzy_probability


def perform_exchange(
    wealth_1: float,
    wealth_2: float,
):
    production = production_coefficient * (wealth_1 + wealth_2)
    production_tax_gov = production_tax * production
    production = production - production_tax_gov
    total_fuzzy = (
        wealth_1**exchange_fuzzy_probability + wealth_2**exchange_fuzzy_probability
    )
    new_wealth_1 = (wealth_1**exchange_fuzzy_probability) * production / total_fuzzy
    new_wealth_2 = (wealth_2**exchange_fuzzy_probability) * production / total_fuzzy

    return new_wealth_1, new_wealth_2, production_tax_gov


def expected_exchange(wealth_1: np.array, wealth_2: np.array) -> np.array:
    production = production_coefficient * wealth_1 + wealth_2
    production_tax_gov = production_tax * production
    production = production - production_tax_gov
    total_fuzzy = (
        wealth_1**exchange_fuzzy_probability + wealth_2**exchange_fuzzy_probability
    )
    new_wealth_1 = wealth_1**exchange_fuzzy_probability / total_fuzzy * production
    return new_wealth_1
