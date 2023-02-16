import numpy as np


def calculate_migration_probability(array: np.array, goverment_help: np.array):
    government_average = np.array(
        [array[array[1] == state, 2].avg() for state in range(50)]
    )

    possible_state_array = np.random.choice(50, array.size, replace=True)


def make_migration_father(array, possible_state_array, government_help):
    array_c = np.c_[array, possible_state_array, np.zeros(array.size)]
    array_c[:, 4] = array_c.apply(
        lambda x: calculate_expected_value(x[2], x[3], government_help), axis=1
    )
    array_c[:, 2] = array_c.apply(
        lambda x: calculate_expected_value(x[2], x[1], government_help), axis=1
    )
    array[:, 1] = array_c.apply(lambda x: make_migration(x[3], x[2], x[4]))
    return array


def make_migration(observed_state, value_state, value_new_state) -> np.array:
    pass
