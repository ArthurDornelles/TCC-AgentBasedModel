import numpy as np

from src.calculations.sampling import sample
from src.calculations.exchange import perform_exchange
from src.calculations.living_cost import living_cost_calculation
from src.calculations.government_help import government_help_by_state
from src.utils.Log import Logger

global logger
logger = Logger()


def make_iterations(array: np.array, iterations: int) -> np.array:
    for iteration in range(iterations):

        array, state_tax_collected = make_transaction(array, sample(array))

        array = living_cost_calculation(array)

        array = add_government_help(array, state_tax_collected)

        array = migration(array)
        logger.info(f"Finished iteration {iteration+1}")

    print(array)


def make_transaction(array: np.array, sampling_array: np.array) -> np.array:
    """ """
    count = 0
    state_tax_collected = {}
    for state in sampling_array:
        state_tax_collected[count] = 0
        for index_1, index_2 in state:
            w_1_new, w_2_new, w_gov = perform_exchange(
                array[array[:, 0] == index_1, 2], array[array[:, 0] == index_2, 2]
            )
            array[array[:, 0] == index_1, 2] = (
                array[array[:, 0] == index_1, 2] + w_1_new
            )
            array[array[:, 0] == index_2, 2] = (
                array[array[:, 0] == index_2, 2] + w_2_new
            )
            state_tax_collected[count] += w_gov
        count += 1
    return array, state_tax_collected


def add_government_help(array: np.array, state_tax_collected: dict) -> np.array:
    for state in state_tax_collected.keys():
        array[array[:, 1] == state, 2] = government_help_by_state(
            array[array[:, 1] == state, 2], state_tax_collected[state]
        )
    return array


def migration(array: np.array) -> np.array:
    return array
