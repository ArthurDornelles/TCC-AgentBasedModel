import numpy as np


def sample(array: np.array) -> np.array:
    """Returns a random order of the index for transaction
    - each row is a state and each pair of columns is a combination
    array[1,0:2] is a combination
    """
    sampling_array = check_even_size_state_array(
        np.array(
            [
                np.random.choice(
                    array[array[:, 1] == state][:, 0],
                    size=array[array[:, 1] == state][:, 0].size,
                    replace=False,
                )
                for state in np.sort(np.unique(array[:, 1]))
            ]
        )
    )

    sampling_transaction_array = np.array(
        [
            np.array([transaction for transaction in zip(state[::2], state[1::2])])
            for state in sampling_array
        ]
    )

    return sampling_transaction_array


def check_even_size_state_array(array: np.array) -> np.array:
    array = np.array([state if len(state) % 2 == 0 else state[:-1] for state in array])
    return array
