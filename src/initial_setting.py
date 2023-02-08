import numpy as np


def set_initial_array(
    number_of_states: int, number_of_people_by_state: int
) -> np.array:
    """ """
    total_people = number_of_states * number_of_people_by_state
    initial_wealth = 100
    wealth = np.random.normal(
        initial_wealth,
        initial_wealth / 10,
        total_people,
    )
    array = np.array(
        [
            [index, index // number_of_people_by_state, np.around(wealth, 0)]
            for index, wealth in zip(range(total_people), wealth)
        ]
    )
    return array
