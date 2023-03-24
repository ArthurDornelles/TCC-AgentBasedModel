import numpy as np

from config import exchange_fuzzy_probability


def sample(array: np.array) -> np.array:
    """Returns a random order of the index for transaction
    - each line contains the state of transaction, agent_1 and agent_2.
    """
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
    sampling_array = np.array(
        [
            np.array(
                [
                    agent_state,
                    *np.random.choice(
                        array[array[:, 1] == agent_state][:, 0],
                        size=2,
                        replace=False,
                        p=probability_array(array[array[:, 1] == agent_state]),
                    ),
                ]
            )
            for agent_state in sampling_array[0]
        ]
    )

    return sampling_array


def probability_array(array: np.array) -> np.array:
    sqrt_array = array[:, 2] ** exchange_fuzzy_probability
    probability_array = sqrt_array / sqrt_array.sum()
    return probability_array
