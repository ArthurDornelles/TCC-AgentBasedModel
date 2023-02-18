import pandas as pd

from config import (
    number_of_states,
    total_people,
    iterations,
    production_tax,
    production_coefficient,
    migration_coefficient,
    exchange_fuzzy_coefficient,
    phi,
)
from src.connections.connections import DatabaseConnection


def save_df_to_db(df: pd.DataFrame, table_name) -> None:
    conn = DatabaseConnection().connect()
    df.to_sql(table_name, con=conn, if_exists="append")


def save_config_to_db(config_table_name: str) -> None:
    conn = DatabaseConnection().connect()
    df = pd.DataFrame(
        [
            [
                "number_of_states",
                number_of_states,
            ],
            ["total_people", total_people],
            ["iterations", iterations],
            ["production_tax", production_tax],
            ["production_coefficient", production_coefficient],
            ["migration_coefficient", migration_coefficient],
            ["exchange_fuzzy_coefficient", exchange_fuzzy_coefficient],
            ["phi", phi],
        ],
        columns=["Property", "Value"],
    )
    df.to_sql(config_table_name, conn, if_exists="replace")
