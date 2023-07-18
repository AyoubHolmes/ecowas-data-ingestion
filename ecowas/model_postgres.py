import psycopg2
from psycopg2 import OperationalError
from ecowas.custom_logger import CustomLogger


logging = CustomLogger("POSTGRES MODEL")


class PostgresModel:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        try:
            # Connect to the default postgres database to check if the database exists
            self.connection = psycopg2.connect(
                database="postgres",
                user=self.config.POSTGRES_USER,
                password=self.config.POSTGRES_PASSWORD,
                host=self.config.POSTGRES_HOST,
                port=self.config.POSTGRES_PORT,
            )
            self.connection.autocommit = True
            self._create_db_if_not_exists()
            self.connection.close()
            # Reconnect to the database
            self.connection = psycopg2.connect(
                database=self.config.POSTGRES_DB,
                user=self.config.POSTGRES_USER,
                password=self.config.POSTGRES_PASSWORD,
                host=self.config.POSTGRES_HOST,
                port=self.config.POSTGRES_PORT,
            )
            self.connection.autocommit = True
            logging.info("Connected to the Database Successfully! :)")
        except OperationalError as e:
            logging.error(
                f"An error occurred while connecting to the database: {str(e)}"
            )

    def _create_db_if_not_exists(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{self.config.POSTGRES_DB}';")
        exists = cursor.fetchone()
        # Create the database if it doesn't exist
        if not exists:
            cursor.execute(f"CREATE DATABASE {self.config.POSTGRES_DB};")
            logging.info(f"Created database {self.config.POSTGRES_DB}")
        else:
            logging.info(f"Database {self.config.POSTGRES_DB} already exists")
        cursor.close()

    
    
