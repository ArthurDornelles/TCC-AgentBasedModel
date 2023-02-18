import numpy as np

from src.calculations.exchange import expected_exchange
from src.calculations.living_cost import weight_function_array_average

from config import migration_coefficient, exchange_fuzzy_coefficient


def perform_migration(array: np.array, state_tax_collected: dict):
    government_average = {
        int(state): array[array[:, 1] == state, 2].mean()
        for state in np.sort(np.unique(array[:, 1]))
    }

    possible_state_array = np.random.choice(
        np.unique(array[:, 1]), len(array), replace=True
    )

    array = make_migration(
        array, possible_state_array, government_average, state_tax_collected
    )

    return array


def make_migration(
    array: np.array,
    possible_state_array: np.array,
    government_average: np.array,
    government_help: dict,
):
    # 0-index, 1-state, 2-wealth,3-exchange, 4-possible_state,
    # 5- exchange_probability, 6-possible_exchange_probability
    # 7-possible_exchange 8-cost, 9-possible_cost, 10-government_help,
    #  11-expected_government_help,  12 - gain, 13-possible_gain

    # adds possible_state_array
    array_c = np.array(array, copy=True)
    government_average_array = np.array(
        [government_average[int(state)] for state in array_c[:, 1]]
    )
    # 3 and 4
    array_c = np.c_[
        array_c,
        expected_exchange(array_c[:, 2], government_average_array),
        possible_state_array,
    ]
    exchange_probability_array = {
        state: (array_c[array_c[:, 1] == state] ** (exchange_fuzzy_coefficient)).sum()
        * array_c[array_c[:, 1] == state].size
        for state in np.unique(array_c[:, 1])
    }
    # 5, 6
    array_c = np.c_[
        array_c,
        np.array(
            [float(exchange_probability_array[int(state)]) for state in array_c[:, 1]]
        ),
        np.array(
            [float(exchange_probability_array[int(state)]) for state in array_c[:, 4]]
        ),
    ]
    possible_gov_average_array = np.array(
        [government_average[int(state)] for state in array_c[:, 4]]
    )
    # 7, 8, 9, 10, 11
    array_c = np.c_[
        array_c,
        expected_exchange(array_c[:, 2], possible_gov_average_array),
        weight_function_array_average(
            array_c[:, 2], government_average_array, array_c[:, 5]
        ),
        weight_function_array_average(
            array_c[:, 2], possible_gov_average_array, array_c[:, 6]
        ),
        np.array([float(government_help[int(state)]) for state in array_c[:, 1]]),
        np.array([float(government_help[int(state)]) for state in array_c[:, 4]]),
    ]
    # 12, 13
    array_c = np.c_[
        array_c,
        array_c[:, 3] - array_c[:, 8] + array_c[:, 10],
        array_c[:, 7] - array_c[:, 9] + array_c[:, 11],
    ]
    choose_if_migrate_v = np.vectorize(choose_if_migrate)
    array[:, 1] = choose_if_migrate_v(
        array_c[:, 12], array_c[:, 13], array_c[:, 1], array_c[:, 4]
    )
    return array


def choose_if_migrate(
    gain: float, gain_new_state: float, state: int, new_state: int
) -> int:
    return np.random.choice(
        [state, new_state],
        size=1,
        replace=False,
        p=calculate_migration_probability(gain, gain_new_state),
    )[0]


def calculate_migration_probability(value: float, value_new: float) -> float:
    if not value_new or value > value_new:
        return [1, 0]
    return [
        1 - np.exp(-value / (migration_coefficient * value_new)),
        np.exp(-value / (migration_coefficient * value_new)),
    ]
