import numpy as np

from config import exchange_fuzzy_probability


def sample(array: np.array) -> np.array:
    """Returns a random order of the index for transaction
    - each row is a state and each pair of columns is a combination
    array[1,0:2] is a combination
    """
    sampling_array = check_even_size_state_array(
        {
            state: np.random.choice(
                array[array[:, 1] == state][:, 0],
                size=array[array[:, 1] == state][:, 0].size,
                replace=True,
                p=probability_array(array, state),
            )
            for state in np.sort(np.unique(array[:, 1]))
        }
    )

    sampling_transaction_array = {
        state_key: np.array(
            [transaction for transaction in zip(state_array[::2], state_array[1::2])]
        )
        for state_key, state_array in sampling_array.items()
    }

    return sampling_transaction_array


def check_even_size_state_array(array: dict[np.array]) -> dict:
    array = {
        state: array[state] if len(array[state]) % 2 == 0 else array[state][:-1]
        for state in array.keys()
    }
    return array


def probability_array(array: np.array, state: int) -> np.array:
    sqrt_array = array[array[:, 1] == state][:, 2] ** exchange_fuzzy_probability
    probability_array = sqrt_array / sqrt_array.sum()
    return probability_array
