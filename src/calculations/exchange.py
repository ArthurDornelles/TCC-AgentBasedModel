import numpy as np


def transaction_exchange(
    wealth_1: float,
    wealth_2: float,
    production_coefficient: float,
    production_tax_coef: float,
):
    production = production_coefficient * (wealth_1 + wealth_2)
    production_tax = production_tax_coef * production
    production = production - production_tax
    new_wealth_1 = wealth_1 / (wealth_1 + wealth_2) * production
    new_wealth_2 = wealth_2 / (wealth_1 + wealth_2) * production
    return new_wealth_1, new_wealth_2, production_tax
