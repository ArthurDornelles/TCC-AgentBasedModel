import numpy as np

from src.analysis.statistics import (
    get_iteration_statistics,
    get_iteration_flux_statistics,
)
from src.calculations.sampling import sample
from src.calculations.exchange import perform_exchange
from src.calculations.living_cost import living_cost_calculation
from src.calculations.government_help import (
    government_help_by_state,
    government_help_negative_people,
)
from config import (
    production_tax,
    production_value,
    iterations_to_migration,
    number_of_states,
)
from src.connections.insert import save_df_to_db
from src.utils.Log import Logger
from src.calculations.migration import perform_migration
from src.initial_setting import set_states_tax_collection

global logger
logger = Logger()


def make_iterations(
    array: np.array, iterations: int, table: str, state_tax_collected: dict
) -> np.array:
    logger.info(f"Finished setting")

    for iteration in range(iterations):
        logger.info(f"Starting iteration {iteration+1}")
        array, state_tax_collected = make_transaction(
            array, sample(array), state_tax_collected
        )
        logging_tax = state_tax_collected.copy()
        if not ((iteration + 1) % iterations_to_migration):
            logger.info(f"Finished transaction, starting living cost")
            array = living_cost_calculation(array)

            logger.info(f"Finished living cost, starting government help")
            array, state_tax_collected = add_government_help(array, state_tax_collected)
            logger.info(f"Finished government help, starting migration")

            array = perform_migration(array, state_tax_collected)
            logger.info(f"Finished migration, starting analysis")

            df_flux_analysis = get_iteration_flux_statistics(array, iteration)
            save_df_to_db(df_flux_analysis, table.flux_table_name)

            # remembers this wealth for next migration
            array[:, 3:5] = array[:, 1:3]

        df_analysis = get_iteration_statistics(array, logging_tax, iteration)
        logger.info(f"Saving analysis")

        save_df_to_db(df_analysis, table.iter_table_name)
        logger.info(f"Finished iteration {iteration+1}")

    print(array)


def make_transaction(
    array: np.array, sampling_array: np.array, state_tax_collected: dict
) -> np.array:
    """ """
    state_tax_collected = {
        int(state): state_tax_collected[state]
        + sampling_array[sampling_array[:, 0] == state, 0].size
        * (production_value * production_tax)
        for state in np.unique(array[:, 1])
    }
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
    state_tax_collected = set_states_tax_collection(number_of_states)
    return array, state_tax_collected
