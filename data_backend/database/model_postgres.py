from sqlalchemy import create_engine, text

from data_backend.custom_logger import CustomLogger
from data_backend.database.table_definitions import Base

logging = CustomLogger("POSTGRES MODEL")


class PostgresModel:
    def __init__(self, config):
        self.config = config
        self.engine = None

    def connect(self):
        db_connection_string = (
            f"postgresql://{self.config.POSTGRES_USER}:{self.config.POSTGRES_PASSWORD}"
            f"@{self.config.POSTGRES_HOST}:{self.config.POSTGRES_PORT}/{self.config.POSTGRES_DB}"
        )
        try:
            self.engine = create_engine(db_connection_string)
            connection = self.engine.connect()
            connection.close()
            logging.info("Connected to the Database Successfully! :)")
            return self.engine
        except Exception as e:
            logging.error(
                f"An error occurred while connecting to the database: {str(e)}"
            )
            logging.error("Exiting...")
            exit(1)

    def re_create_tables(self, tables: list):
        try:
            for t in tables:
                self.delete_table(t)
            Base.metadata.create_all(self.engine, checkfirst=True)
            logging.info("Created tables successfully!")
        except Exception as e:
            logging.error(f"An error occurred while creating tables: {str(e)}")

    def delete_table(self, table):
        try:
            if self.table_exists(table):
                table.__table__.drop(self.engine, checkfirst=True)
                logging.info(f"Deleted table {table.__tablename__}")
            else:
                logging.info(f"Cannot Delete Table {table.__tablename__} it does not exist!")
        except Exception as e:
            logging.error(f"An error occurred while deleting tables: {str(e)}")

    def table_exists(self, table_cls):
        with self.engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT EXISTS (SELECT 1 FROM pg_tables WHERE tablename = '{table_cls.__tablename__}')"))
            return result.scalar()
