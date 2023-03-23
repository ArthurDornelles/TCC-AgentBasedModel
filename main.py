from config import number_of_states, total_people, iterations
from src.initial_setting import set_initial_array, set_states_tax_collection
from src.utils.Log import Logger, TableNames
from src.iterations import make_iterations

global logger, table_names
logger = Logger()
table_names = TableNames()


def main() -> None:
    logger.info(
        f"Starting initial array for {total_people} persons, {number_of_states} states and {iterations} iterations"
    )
    array = set_initial_array(
        number_of_states, total_people, table_names.config_table_name
    )
    state_tax_collected = set_states_tax_collection(number_of_states)
    array = make_iterations(
        array, iterations, table_names.table_name, state_tax_collected
    )
    logger.info(f"Finished all {iterations} iterations")


if __name__ == "__main__":
    main()
