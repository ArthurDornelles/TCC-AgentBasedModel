import numpy as np
import pandas as pd

from src.analysis.statistics import (
    get_iteration_statistics,
    get_iteration_flux_statistics,
)
from src.calculations.sampling import sample
from src.calculations.exchange import make_transaction
from src.calculations.living_cost import living_cost_calculation
from src.calculations.government_help import add_government_help
from config import iterations_to_migration
from src.connections.insert import save_df_to_db
from src.utils.Log import Logger
from src.calculations.migration import perform_migration

global logger
logger = Logger()


def make_iterations(
    array: np.array, iterations: int, table: str, state_tax_collected: dict
) -> np.array:
    logger.info(f"Finished setting")

    for iteration in range(iterations):
        logger.info(f"Starting iteration {iteration+1}")
        sampling = sample(array)

        logger.info(f"Finished sampling")
        array, state_tax_collected = make_transaction(
            array, sampling, state_tax_collected
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

            # remembers this state and wealth for next migration
            array[:, 3:5] = array[:, 1:3]

        df_analysis = get_iteration_statistics(array, logging_tax, iteration)
        logger.info(f"Saving analysis")

        save_df_to_db(df_analysis, table.iter_table_name)
        logger.info(f"Finished iteration {iteration+1}")

    print(array)
