import numpy as np

from config import number_of_states
from src.initial_setting import set_states_tax_collection


def add_government_help(array: np.array, state_tax_collected: dict) -> np.array:
    for state in state_tax_collected.keys():
        (
            array[(array[:, 1] == state) & (array[:, 2] < 0), 2],
            state_tax_collected[state],
        ) = government_help_negative_people(
            array[(array[:, 1] == state) & (array[:, 2] < 0), 2],
            state_tax_collected[state],
        )
        array[array[:, 1] == state, 2] = government_help_by_state(
            array[array[:, 1] == state, 2], state_tax_collected[state]
        )
    state_tax_collected = set_states_tax_collection(number_of_states)
    return array, state_tax_collected


def government_help_by_state(
    array: np.array, state_total_collection: float
) -> np.array:
    avg_tax_collection = state_total_collection / len(array) if len(array) else 0
    array = array + avg_tax_collection
    return array


def government_help_negative_people(
    array: np.array, state_total_collection: float
) -> np.array:
    """Input array is given by"""
    if array.sum() < -state_total_collection:
        array[:] = 0.01
        return array, 0

    else:
        state_total_collection += float(array.sum())
        array[:] = 0
        return array, state_total_collection
