import numpy as np

from config import initial_wealth
from src.connections.insert import save_config_to_db


def set_initial_array(
    number_of_states, number_of_people_by_state, config_table_name: str
) -> np.array:
    """ """
    save_config_to_db(config_table_name)
    if type(number_of_people_by_state) == int:
        total_people = number_of_states * number_of_people_by_state
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
    if type(number_of_people_by_state) == dict:
        wealth = np.random.normal(
            initial_wealth[0], initial_wealth[0] / 10, number_of_people_by_state[0]
        )
        array = np.array(
            [
                [i_, 0, np.round(wealth, 0), 0, np.round(wealth, 0)]
                for i_, wealth in zip(range(number_of_people_by_state[0]), wealth)
            ]
        )
        i = number_of_people_by_state[0]
        for state, people in list(number_of_people_by_state.items())[1:]:
            wealth = np.random.normal(
                initial_wealth[state], initial_wealth[state] / 10, people
            )
            array_state = np.array(
                [
                    [i_, state, np.round(wealth, 0), state, np.round(wealth, 0)]
                    for i_, wealth in zip(range(i, i + people), wealth)
                ]
            )
            i += people
            array = np.append(array, array_state, axis=0)
        return array


def set_states_tax_collection(number_of_states: int):
    state_tax_collected = {int(state): 0 for state in range(number_of_states)}
    return state_tax_collected
