import numpy as np

from src.connections.insert import save_config_to_db


def set_initial_array(
    number_of_states: int, number_of_people_by_state: int, config_table_name: str
) -> np.array:
    """ """
    save_config_to_db(config_table_name)
    total_people = number_of_states * number_of_people_by_state
    initial_wealth = 100
    wealth = np.random.normal(
        initial_wealth,
        initial_wealth / 10,
        total_people,
    )
    array = np.array(
        [
            [
                index,
                index // number_of_people_by_state,
                np.around(wealth, 0),
                index // number_of_people_by_state,
                np.around(wealth, 0),
            ]
            for index, wealth in zip(range(total_people), wealth)
        ]
    )
    return array


def set_states_tax_collection(number_of_states: int):
    state_tax_collected = {int(state): 0 for state in range(number_of_states)}
    return state_tax_collected
