from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import declarative_base

from data_backend.custom_logger import CustomLogger

logging = CustomLogger("POSTGRES MODEL")


class PostgresModel:
    def __init__(self, config, table_models: declarative_base()):
        self.config = config
        self.base = table_models
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

    def get_table_columns(self, table):
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f"SELECT * FROM {table.__tablename__} LIMIT 0"))
                return result.keys()
        except Exception as e:
            logging.error(f"An error occurred while getting table columns: {str(e)}")

    def re_create_table(self, tables: list):
        try:
            for t in tables:
                self.delete_table(t)
            self.base.metadata.create_all(self.engine, checkfirst=True)
            logging.info(f"Created tables {[t.__tablename__ for t in tables]} successfully!")
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

    def get_one(self, table_cls, **kwargs):
        where_column_name = kwargs.get('where_column')
        select_column_name = kwargs.get('select_column')
        where_value = kwargs.get('where_value')

        if not (where_column_name and select_column_name and where_value):
            raise ValueError(
                "All three parameters 'where_column', 'select_column', and 'where_value' must be specified.")

        where_column = getattr(table_cls.c, where_column_name)
        select_column = getattr(table_cls.c, select_column_name)

        with self.engine.connect() as conn:
            query = select(select_column).where(where_column == where_value)
            result = conn.execute(query)
            row = result.fetchone()
            if row is None:
                return None
            return row[0]  # Access the first element in the row tuple
