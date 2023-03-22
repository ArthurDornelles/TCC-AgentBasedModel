import numpy as np

from src.analysis.statistics import get_iteration_statistics
from src.calculations.sampling import sample
from src.calculations.exchange import perform_exchange
from src.calculations.living_cost import living_cost_calculation
from src.calculations.government_help import (
    government_help_by_state,
    government_help_negative_people,
)
from config import production_tax, production_value
from src.connections.insert import save_df_to_db
from src.utils.Log import Logger
from src.calculations.migration import perform_migration

global logger
logger = Logger()


def make_iterations(array: np.array, iterations: int, table_name: str) -> np.array:
    for iteration in range(iterations):
        logger.info(f"Finished setting, starting iteration {iteration+1}")
        array, state_tax_collected = make_transaction(array, sample(array))

        logger.info(f"Finished transaction, starting living cost ")
        array = living_cost_calculation(array)

        logger.info(f"Finished living cost, starting government help ")
        array = add_government_help(array, state_tax_collected)
        logger.info(f"Finished government help, starting migration ")

        array = perform_migration(array, state_tax_collected)
        logger.info(f"Finished migration, starting analysis")

        df_analysis = get_iteration_statistics(array, state_tax_collected, iteration)
        logger.info(f"Saving analysis")

        save_df_to_db(df_analysis, table_name)

        logger.info(f"Finished iteration {iteration+1}")

    print(array)


def make_transaction(array: np.array, sampling_array: np.array) -> np.array:
    """ """
    state_tax_collected = {
        int(state): sampling_array[sampling_array[:, 0] == state, 0].size
        * (production_value * production_tax)
        for state in np.unique(array[:, 1])
    }
    logger.info("start transaction iteration")
    for _, index_1, index_2 in sampling_array:
        w_1_new, w_2_new = perform_exchange(
            array[array[:, 0] == index_1, 2], array[array[:, 0] == index_2, 2]
        )
        array[array[:, 0] == index_1, 2] = array[array[:, 0] == index_1, 2] + w_1_new
        array[array[:, 0] == index_2, 2] = array[array[:, 0] == index_2, 2] + w_2_new
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
