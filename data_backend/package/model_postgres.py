from data_backend.custom_logger import CustomLogger
from sqlalchemy import create_engine, inspect
from data_backend.package.table_definitions import Base, Country, Kpi, KpiValue

logging = CustomLogger("POSTGRES MODEL")


class PostgresModel:
    def __init__(self, config):
        self.config = config
        self.engine = None
        self.table_classes = [Country, Kpi, KpiValue]

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

    def create_tables_if_not_exists(self):
        try:
            if not all(self._table_exists(t) for t in self.table_classes):
                Base.metadata.create_all(self.engine, checkfirst=True)
                logging.info("Created tables successfully! :)")
            else:
                logging.info("Tables already exist. Moving on...")
        except Exception as e:
            logging.error(f"An error occurred while creating tables: {str(e)}")

    def _table_exists(self, table_cls):
        inspector = inspect(self.engine)
        return inspector.has_table(table_cls.__tablename__)
    
    def load_csv_to_pg(self, csv, table_name, if_exists="fail", index=False):
        try:
            csv.to_sql(table_name, self.engine, if_exists=if_exists, index=index)
            logging.info(f"Table {table_name} loaded successfully!")
        except Exception as e:
            logging.error(f"Failed to load table {table_name}: {e}")
            logging.error("Exiting...")
            exit(1)