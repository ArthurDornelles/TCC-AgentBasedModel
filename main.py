from config import number_of_states, total_people, iterations
from src.initial_setting import set_initial_array
from src.utils.Log import Logger

global logger
logger = Logger()


def main() -> None:

    logger.info(
        f"Starting initial array for {total_people} persons, {number_of_states} states and {iterations} iterations"
    )
    array = set_initial_array(number_of_states, total_people, iterations)


if __name__ == "__main__":
    main()
