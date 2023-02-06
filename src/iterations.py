import numpy as np

from src.calculations.sampling import sample


def make_iterations(array: np.array, iterations: int) -> np.array:
    sampling_array = sample(array)
    make_transaction(array, sampling_array)


def make_transaction(array: np.array, sampling_array: np.array) -> np.array:
    """
        import numpy as np
    array = np.array([[1,2,3,4,5,6,7,8,9,10],[11,12,13,14,15,16,17,18,19,20]])
    for state in array:
        for transaction in zip(state[::2], state[1::2]):
            print(transaction)
    """
    for state_array in sampling_array:
        for transaction in state_array[:, :, 2]:
            pass
