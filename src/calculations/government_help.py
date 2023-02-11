import numpy as np


def government_help_by_state(
    array: np.array, state_total_collection: float
) -> np.array:
    avg_tax_collection = state_total_collection / len(array) if len(array) else 0
    array = array + avg_tax_collection
    return array
