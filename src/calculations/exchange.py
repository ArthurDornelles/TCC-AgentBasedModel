import numpy as np

from config import production_tax, production_coefficient


def perform_exchange(
    wealth_1: float,
    wealth_2: float,
):
    production = production_coefficient * (wealth_1 + wealth_2)
    production_tax_gov = production_tax * production
    production = production - production_tax_gov
    new_wealth_1 = production / 2
    new_wealth_2 = production / 2
    return new_wealth_1, new_wealth_2, production_tax_gov


def expected_exchange(wealth_1: np.array, wealth_2: np.array) -> np.array:
    production = production_coefficient * wealth_1 + wealth_2
    production_tax_gov = production_tax * production
    production = production - production_tax_gov
    new_wealth_1 = production / 2
    return new_wealth_1
