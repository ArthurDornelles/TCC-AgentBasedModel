import logging


class Logger:
    def __init__(self):
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s"
        )

    def info(self, message: str):
        logging.info(message)
