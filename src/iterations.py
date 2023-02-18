import numpy as np

from src.analysis.statistics import get_iteration_statistics
from src.calculations.sampling import sample
from src.calculations.exchange import perform_exchange
from src.calculations.living_cost import living_cost_calculation
from src.calculations.government_help import (
    government_help_by_state,
    government_help_negative_people,
)
from src.connections.insert import save_df_to_db
from src.utils.Log import Logger
from src.calculations.migration import perform_migration

global logger
logger = Logger()


def make_iterations(array: np.array, iterations: int, table_name: str) -> np.array:
    for iteration in range(iterations):
        array, state_tax_collected = make_transaction(array, sample(array))

        array = living_cost_calculation(array)

        array = add_government_help(array, state_tax_collected)

        array = perform_migration(array, state_tax_collected)

        df_analysis = get_iteration_statistics(array, state_tax_collected, iteration)

        save_df_to_db(df_analysis, table_name)

        logger.info(f"Finished iteration {iteration+1}")

    print(array)


def make_transaction(array: np.array, sampling_array: dict[np.array]) -> np.array:
    """ """
    state_tax_collected = {}
    for state_key, state_array in sampling_array.items():
        state_tax_collected[state_key] = 0
        for index_1, index_2 in state_array:
            if index_1 == index_2:
                continue
            w_1_new, w_2_new, w_gov = perform_exchange(
                array[array[:, 0] == index_1, 2], array[array[:, 0] == index_2, 2]
            )
            array[array[:, 0] == index_1, 2] = (
                array[array[:, 0] == index_1, 2] + w_1_new
            )
            array[array[:, 0] == index_2, 2] = (
                array[array[:, 0] == index_2, 2] + w_2_new
            )
            state_tax_collected[state_key] += w_gov
    return array, state_tax_collected


def add_government_help(array: np.array, state_tax_collected: dict) -> np.array:
    for state in state_tax_collected.keys():
        (
            array[(array[:, 1] == state) & (array[:, 2] < 0), 2],
            state_tax_collected[state],
        ) = government_help_negative_people(
            array[(array[:, 1] == state) & (array[:, 2] < 0), 2],
            state_tax_collected[state],
        )
        array[array[:, 1] == state, 2] = government_help_by_state(
            array[array[:, 1] == state, 2], state_tax_collected[state]
        )
    return array
