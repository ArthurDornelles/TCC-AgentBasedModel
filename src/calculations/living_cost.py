import numpy as np

from config import exchange_fuzzy_probability, phi


def living_cost_calculation(array: np.array) -> np.array:
    for state in np.sort(np.unique(array[:, 1])):
        cost = individual_cost(array[array[:, 1] == state])
        array[array[:, 1] == state, 2] = array[array[:, 1] == state, 2] - cost
    return array


def individual_cost(state_array: np.array) -> np.array:
    average = state_array[:, 2].mean()

    cost = weight_function(state_array[:, 2], average)

    return cost


def weight_function(state_array: np.array, average: float) -> np.array:
    state_array = (
        0.2 * average
        + 4.9
        * average
        * (1 + np.tanh((state_array - 2.5 * average) / (phi * average)))
        / 2
    ) * 0.2
    return state_array


def weight_function_array_average(
    state_array: np.array, average: np.array, probability_array: np.array
) -> np.array:
    array = (
        0.2 * average
        + 4.9
        * average
        * (1 + np.tanh((state_array - 2.5 * average) / (phi * average)))
        / 2
    ) * 0.2
    array_probability = array**exchange_fuzzy_probability
    array = array * array_probability / (array_probability + probability_array)
    return array
