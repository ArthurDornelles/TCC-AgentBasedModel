import numpy as np

from config import exchange_fuzzy_probability
from src.utils.Log import Logger

global logger
logger = Logger()


def sample(array: np.array) -> np.array:
    """Returns a random order of the index for transaction
    - each row is a state and each pair of columns is a combination
    array[1,0:2] is a combination
    """
    logger.info("starting sampling 1")
    sampling_array = np.array(
        [
            np.random.choice(
                array[:, 1],
                size=int(array[:, 0].size / 2),
                replace=True,
                p=probability_array(array),
            )
        ]
    )
    logger.info("starting sampling 2")
    sampling_array = np.array(
        [
            np.array(
                [
                    state,
                    *np.random.choice(
                        array[array[:, 1] == state][:, 0],
                        size=2,
                        replace=False,
                        p=probability_array(array[array[:, 1] == state]),
                    ),
                ]
            )
            for state in sampling_array[0]
        ]
    )

    return sampling_array


def sampling_from_state(state: int, state_array: np.array) -> list[int, int]:
    array = np.array(
        [
            state,
            *np.random.choice(
                state_array[:, 0],
                size=2,
                replace=False,
                p=probability_array(state_array),
            ),
        ]
    )
    return array


def probability_array(array: np.array) -> np.array:
    sqrt_array = array[:, 2] ** exchange_fuzzy_probability
    probability_array = sqrt_array / sqrt_array.sum()
    return probability_array
