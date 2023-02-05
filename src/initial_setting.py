import numpy as np


def set_initial_array(
    number_of_states: int, number_of_people_by_state: int, initial_wealth: int
):
    """ """
    array = np.array(
        [
            [state, initial_wealth]
            for state in range(number_of_states)
            for _ in range(number_of_people_by_state)
        ]
    )
