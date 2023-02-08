import numpy as np


def set_initial_array(
    number_of_states: int, number_of_people_by_state: int
) -> np.array:
    """ """
    initial_wealth = 100
    array = np.array(
        [
            [index, index // number_of_people_by_state, initial_wealth]
            for index in range(number_of_people_by_state * number_of_states)
        ]
    )
    return array
