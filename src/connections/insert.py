import pandas as pd

from config import (
    number_of_states,
    people_by_state,
    iterations,
    production_tax,
    production_value,
    migration_coefficient,
    exchange_fuzzy_probability,
    exchange_fuzzy_probability,
    phi,
    pop_density_coefficient,
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
            ["people_by_state", str(people_by_state)],
            ["iterations", iterations],
            ["production_tax", str(production_tax)],
            ["production_value", str(production_value)],
            ["migration_coefficient", migration_coefficient],
            ["exchange_fuzzy_probability", exchange_fuzzy_probability],
            ["exchange_fuzzy_coefficient", exchange_fuzzy_probability],
            ["phi", str(phi)],
            ["pop_density_coefficient", pop_density_coefficient],
        ],
        columns=["Property", "Value"],
    )
    df.to_sql(config_table_name, conn, if_exists="replace")
