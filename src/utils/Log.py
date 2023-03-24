import logging
import datetime


class Logger:
    def __init__(self):
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s"
        )

    def info(self, message: str):
        logging.info(message)


class TableNames:
    def __init__(self):
        now = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M")
        self.iter_table_name = now + "_iter"
        self.config_table_name = now + "_config"
        self.flux_table_name = now + "_flux"
