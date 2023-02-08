from config import production_tax, production_coefficient


def perform_exchange(
    wealth_1: float,
    wealth_2: float,
):
    production = production_coefficient * (wealth_1 + wealth_2)
    production_tax_gov = production_tax * production
    production = production - production_tax_gov
    new_wealth_1 = wealth_1 / (wealth_1 + wealth_2) * production
    new_wealth_2 = wealth_2 / (wealth_1 + wealth_2) * production
    return new_wealth_1, new_wealth_2, production_tax_gov
