import numpy as np

from src.calculations.sampling import sample


def make_iterations(array: np.array, iterations: int) -> np.array:
    sampling_array = sample(array)
    make_transaction(array, sampling_array)


def make_transaction(array: np.array, sampling_array: np.array) -> np.array:
    pass
