import os
import sqlalchemy

from dotenv import load_dotenv, find_dotenv


class DatabaseConnection:
    def __init__(self):
        load_dotenv(find_dotenv(filename=".env"))
        self.connection_string = os.getenv("DATABASE_URL")

    def connect(self) -> sqlalchemy.engine.base.Engine:
        self.engine = sqlalchemy.create_engine(self.connection_string)
        return self.engine.connect()
