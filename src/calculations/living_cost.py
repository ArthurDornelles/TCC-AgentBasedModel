import numpy as np

from config import phi, number_of_states, total_people, pop_density_coefficient


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
        0.8 * average + 2 * average * np.tanh(state_array / average - 1) / 2
    ) * np.exp(
        pop_density_coefficient * (state_array.size) / (total_people * number_of_states)
    )
    return state_array


def weight_function_array_average(
    wealth_array: np.array,
    state_avg_array: np.array,
    people_by_state_array: np.array,
) -> np.array:
    array = (
        (
            0.2 * state_avg_array
            + 4.9
            * state_avg_array
            * (
                1
                + np.tanh(
                    (wealth_array - 2.5 * state_avg_array) / (phi * state_avg_array)
                )
            )
            / 2
        )
        * people_by_state_array
        * pop_density_coefficient
        / (total_people * number_of_states)
    )
    return array
