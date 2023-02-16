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
    state_array = (
        0.1 * average
        + 9.9 * average * (1 + np.tanh((state_array / 5 * average - 1))) / 2
    )
    return state_array


def weight_function_array_average(state_array: np.array, average: np.array) -> np.array:
    array = (
        0.1 * average
        + 9.9 * average * (1 + np.tanh((state_array * average / 5 - 1))) / 2
    )
    return array
