import numpy as np
import pandas as pd

from config import production_tax, production_value, exchange_fuzzy_probability


def make_transaction(
    array: np.array, sampling_array: np.array, state_tax_collected: dict
) -> np.array:
    """ """
    state_tax_collected = {
        int(state): state_tax_collected[state]
        + sampling_array[sampling_array[:, 0] == state, 0].size
        * (production_value * production_tax)
        for state in np.unique(array[:, 1])
    }
    sampling_array = np.c_[
        sampling_array,
        np.array([array[array[:, 0] == agent][0][2] for agent in sampling_array[:, 1]]),
        np.array([array[array[:, 0] == agent][0][2] for agent in sampling_array[:, 2]]),
    ]
    perform_exchange_v = np.vectorize(perform_exchange)
    sampling_array = np.c_[
        sampling_array,
        perform_exchange_v(sampling_array[:, 3], sampling_array[:, 4]),
        perform_exchange_v(sampling_array[:, 4], sampling_array[:, 3]),
    ]
    df = (
        (
            pd.DataFrame(
                np.append(
                    np.append(
                        sampling_array[:, [1, 5]], sampling_array[:, [2, 6]], axis=0
                    ),
                    np.c_[array[:, 0], np.zeros(array[:, 0].size)],
                    axis=0,
                ),
                columns=["agent", "new_value"],
            )
            .groupby(by="agent")
            .sum()
        )
        .reset_index()
        .sort_values(by="agent")
    )
    new_value_array = df["new_value"].to_numpy()
    array[:, 2] = array[:, 2] + new_value_array

    return array, state_tax_collected


def perform_exchange(
    wealth_1: float,
    wealth_2: float,
) -> float:
    production = production_value * (1 - production_tax)
    total_fuzzy = (
        wealth_1**exchange_fuzzy_probability + wealth_2**exchange_fuzzy_probability
    )
    new_wealth_1 = (
        (wealth_1**exchange_fuzzy_probability) * production / total_fuzzy
        if wealth_1 > 0
        else wealth_1
    )

    return new_wealth_1
