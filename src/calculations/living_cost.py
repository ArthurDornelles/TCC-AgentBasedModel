import numpy as np


def living_cost_calculation(array: np.array) -> np.array:
    for state in range(50):
        cost = individual_cost(array[array[:, 1] == state])
        array[array[:, 1] == state, 2] = array[array[:, 1] == state, 2] - cost
    return array


def individual_cost(state_array: np.array) -> np.array:
    average = state_array[:, 2].mean()

    cost = weight_function(state_array[:, 2], average)

    return cost


def weight_function(state_array: np.array, average: float) -> np.array:
    state_array = np.where(
        state_array >= average * 10,
        average * 10 * 0.15,
        np.where(state_array <= 0.10, average * 0.1 * 0.15, state_array * 0.15),
    )
    return state_array
