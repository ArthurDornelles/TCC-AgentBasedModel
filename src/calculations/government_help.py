import numpy as np


def government_help_by_state(
    array: np.array, state_total_collection: float
) -> np.array:
    avg_tax_collection = state_total_collection / len(array) if len(array) else 0
    array = array + avg_tax_collection
    return array


def government_help_negative_people(
    array: np.array, state_total_collection: float
) -> np.array:
    if array.sum() < -state_total_collection:
        raise ("Government can't keep up!")
    else:
        state_total_collection += float(array.sum())
        array[:] = 0
        return array, state_total_collection
