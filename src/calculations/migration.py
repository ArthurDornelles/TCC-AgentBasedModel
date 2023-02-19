import numpy as np

from src.calculations.exchange import expected_exchange
from src.calculations.living_cost import weight_function_array_average

from config import migration_coefficient, exchange_fuzzy_probability


def perform_migration(array: np.array, state_tax_collected: dict):
    state_avg_dict = {
        int(state): array[array[:, 1] == state, 2].mean()
        for state in np.sort(np.unique(array[:, 1]))
    }
    # state help by agent
    state_help_dict = get_individual_state_help(array, state_tax_collected)
    new_state_array = np.random.choice(np.unique(array[:, 1]), len(array), replace=True)

    array = make_migration(array, new_state_array, state_avg_dict, state_help_dict)

    return array


def make_migration(
    array: np.array,
    new_state_array: np.array,
    state_avg_dict: dict,
    state_help_dict: dict,
):

    # 0-index, 1-state, 2-wealth, 3-new_state, 4-state_samp_probability
    # 5-new_state_samp_probability, 6-expected_exchange, 7-new_expected_exchange
    # 8-state_cost, 9-new_state_cost, 10-state_help, 11-new_state_help
    # 12-gain, 13-new_state_gain

    # adds possible_state_array
    array_c = np.array(array, copy=True)
    array_c[array_c[:, 2] == 0, 2] = 0.01

    # 3 - includes new state
    array_c = np.c_[array_c, new_state_array]
    exchange_probability_dict = {
        state: exchange_probability(array_c, state)
        for state in np.unique(array_c[:, 1])
    }
    # 4-state_samp_probability, 5-state_samp_probability
    array_c = np.c_[
        array_c,
        np.array(
            [float(exchange_probability_dict[int(state)]) for state in array_c[:, 1]]
        ),
        np.array(
            [float(exchange_probability_dict[int(state)]) for state in array_c[:, 3]]
        ),
    ]
    state_avg_array = np.array([state_avg_dict[int(state)] for state in array_c[:, 1]])
    new_state_avg_array = np.array(
        [state_avg_dict[int(state)] for state in array_c[:, 3]]
    )
    number_of_people_by_state = {
        state: array_c[array_c[:, 1] == state, 1].size
        for state in np.unique(array_c[:, 1])
    }
    # calculates the number of people by state and makes it into an array
    gov_n_of_people_array = np.array(
        [
            [number_of_people_by_state[int(state)] for state in array_c[:, 1]],
            [number_of_people_by_state[int(state)] for state in array_c[:, 3]],
        ],
    )
    # 6-state_expected_gain, 7-new_state_expected_gain
    array_c = np.c_[
        array_c,
        expected_exchange(
            array_c[:, 2], state_avg_array, array_c[:, 4], gov_n_of_people_array[0, :]
        ),
        expected_exchange(
            array_c[:, 2],
            new_state_avg_array,
            array_c[:, 5],
            gov_n_of_people_array[1, :],
        ),
    ]

    # 8-state_cost, 9-new_state_cost, 10-state_help, 11-new_state_help
    array_c = np.c_[
        array_c,
        weight_function_array_average(
            array_c[:, 2], state_avg_array, gov_n_of_people_array[0, :]
        ),
        weight_function_array_average(
            array_c[:, 2], new_state_avg_array, gov_n_of_people_array[1, :]
        ),
        np.array([float(state_help_dict[int(state)]) for state in array_c[:, 1]]),
        np.array([float(state_help_dict[int(state)]) for state in array_c[:, 3]]),
    ]

    # 12-state_expected_gain, 13-new_state_expected_gain
    array_c = np.c_[
        array_c,
        array_c[:, 6] - array_c[:, 8] + array_c[:, 10],
        array_c[:, 7] - array_c[:, 9] + array_c[:, 11],
    ]
    if len(array_c[np.isnan(array_c[:, 12]), :]) or len(
        array_c[np.isnan(array_c[:, 13]), :]
    ):
        print("help, fuck!")
    choose_if_migrate_v = np.vectorize(choose_if_migrate)
    array[:, 1] = choose_if_migrate_v(
        array_c[:, 12], array_c[:, 13], array_c[:, 1], array_c[:, 3]
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
    if value < 0 and value_new > 0:
        return [0, 1]
    return [
        1 - np.exp(-value / (migration_coefficient * value_new)),
        np.exp(-value / (migration_coefficient * value_new)),
    ]


def get_individual_state_help(array: np.array, state_tax_collected: dict) -> dict:
    state_indv_help = {
        state: state_tax_collected[int(state)] / (array[array[:, 1] == state, 0].size)
        for state in np.unique(array[:, 1])
    }
    return state_indv_help


def exchange_probability(array_c: np.array, state: float) -> np.array:
    return (array_c[array_c[:, 1] == state, 2] ** exchange_fuzzy_probability).sum()
