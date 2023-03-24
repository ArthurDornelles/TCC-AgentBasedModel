import math
import numpy as np

from config import migration_coefficient


def perform_migration(array: np.array, state_tax_collected: dict):
    states_average = {
        state: array[array[:, 1] == state, 2].mean() for state in np.unique(array[:, 1])
    }
    array_c = np.c_[array, np.array([states_average[state] for state in array[:, 1]])]
    for agent in array:
        agent_diff = agent[2] - agent[4]
        comparative_agents = array_c[
            (
                (array_c[:, 4] - array_c[:, 5] / 200 <= agent[2])
                & (array_c[:, 4] + array_c[:, 5] / 200 >= agent[2])
            )
            & ~(array[:, 1] == agent[1]),
            :,
        ]
        comparative_states_average = {
            state: [
                (
                    comparative_agents[comparative_agents[:, 1] == state, 2]
                    - comparative_agents[comparative_agents[:, 1] == state, 4]
                ).mean(),
                comparative_agents[comparative_agents[:, 1] == state, 2].size,
            ]
            for state in np.unique(comparative_agents[:, 1])
            if agent_diff
            <= (
                comparative_agents[comparative_agents[:, 1] == state, 2]
                - comparative_agents[comparative_agents[:, 1] == state, 4]
            ).mean()
        }
        if not len(comparative_states_average):
            continue
        comparative_agents = comparative_agents[
            np.isin(comparative_agents[:, 1], list(comparative_states_average.keys()))
        ]
        all_comparative_average = (
            comparative_agents[:, 2] - comparative_agents[:, 4]
        ).mean()

        array[array[:, 0] == agent[0], 1] = choose_if_migrate(
            agent_diff, all_comparative_average, agent[1], comparative_states_average
        )

    return array


def choose_if_migrate(
    gain: float, gain_new_state: float, state: int, comparative_states_average: int
) -> int:
    if math.isnan(gain_new_state):
        return state
    if np.random.choice(
        [True, False],
        size=1,
        replace=False,
        p=calculate_migration_probability(gain, gain_new_state),
    )[0]:
        return state
    else:
        states = [states for states, _ in comparative_states_average.items()]
        values = np.array(
            [values[0] for _, values in comparative_states_average.items()]
        )
        return np.random.choice(
            states,
            size=1,
            replace=False,
            p=values / values.sum(),
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
