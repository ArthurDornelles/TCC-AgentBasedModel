import numpy as np

from src.calculations.sampling import sample
from src.calculations.exchange import perform_exchange
from src.utils.Log import Logger

global logger
logger = Logger()


def make_iterations(array: np.array, iterations: int) -> np.array:
    for iteration in range(iterations):
        array = make_transaction(array, sample(array))
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
    return array
