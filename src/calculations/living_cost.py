import numpy as np

from config import number_of_states, people_by_state, pop_density_coefficient, phi


def living_cost_calculation(array: np.array) -> np.array:
    for state in np.sort(np.unique(array[:, 1])):
        cost = individual_cost(array[array[:, 1] == state], state)
        array[array[:, 1] == state, 2] = array[array[:, 1] == state, 2] - cost
    return array


def individual_cost(state_array: np.array, state: float) -> np.array:
    average = state_array[:, 2].mean()
    state_phi = phi if type(phi) == float else phi[state]

    cost = weight_function(state_array[:, 2], average, state_phi, get_total_people())

    return cost


def weight_function(
    state_array: np.array, average: float, state_phi: float, total_people: int
) -> np.array:
    state_array = (
        state_phi
        * (0.8 * average + 2 * average * np.tanh(state_array / average - 1) / 2)
        * np.exp(pop_density_coefficient * (state_array.size) / (total_people))
    )
    return state_array


def get_total_people() -> int:
    if type(people_by_state) == int:
        return people_by_state * number_of_states
    elif type(people_by_state) == dict:
        return np.array(list(people_by_state.items())).sum()
