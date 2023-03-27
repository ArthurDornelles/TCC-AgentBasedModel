import pandas as pd
import numpy as np


def get_iteration_statistics(
    array: np.array, state_tax_collection: dict, iteration: int
) -> pd.DataFrame:
    df = pd.DataFrame(
        [
            {
                "Iteration": iteration,
                "State": int(state),
                "People": len(array[array[:, 1] == state]),
                "Avg Wealth": array[array[:, 1] == state, 2].mean(),
                "Median Wealth": np.median(array[array[:, 1] == state, 2]),
                "Std Dev Wealth": array[array[:, 1] == state, 2].std(),
                "Max Wealth": array[array[:, 1] == state, 2].max(),
                "Min Wealth": array[array[:, 1] == state, 2].min(),
                "State Tax Collection": state_tax_collection[int(state)],
            }
            for state in np.sort(np.unique(array[:, 1]))
        ],
    )
    return df


def get_iteration_flux_statistics(array: np.array, iteration: int) -> pd.DataFrame:
    array = array[~(array[:, 1] == array[:, 3])][:, [1, 2, 3]]
    df = pd.DataFrame(array, columns=["origin", "wealth_mean", "destination"])
    df["iteration"] = iteration
    df["count"] = 1
    df = df.groupby(by=["origin", "destination", "iteration"]).agg(
        {"wealth_mean": "mean", "count": "sum"}
    )
    return df
