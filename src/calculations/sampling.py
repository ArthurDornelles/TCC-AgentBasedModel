import numpy as np


def sample(array: np.array) -> np.array:
    """Returns a random order of the index for transaction
    - each row is a state and each pair of columns is a combination
    array[1,0:2] is a combination
    """
    sampling_array = np.array(
        [
            np.random.choice(
                array[array[:, 1] == state][:, 0],
                size=array[array[:, 1] == state][:, 0].size,
                replace=False,
            )
            for state in np.sort(np.unique(array[:, 1]))
        ]
    )
    return sampling_array
