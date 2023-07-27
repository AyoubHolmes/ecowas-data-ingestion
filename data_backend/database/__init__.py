from sqlalchemy.orm import declarative_base

from data_backend.custom_logger import CustomLogger

logging = CustomLogger("database")


class Database:
    def __init__(self, config, table_definitions: declarative_base()):
        self.config = config
        self.base = table_definitions
        self.model = None
        self.engine = None

    def create_connection(self):
        if self.config is None:
            raise ValueError("Configuration is not initialized. Call init() first.")

        self.model = self._get_dbs_model()
        self.engine = self.model.connect()

    def _get_dbs_model(self):
        if self.config.DATABASE_SYSTEM == "postgres":
            from data_backend.database.model_postgres import PostgresModel
            model = PostgresModel(self.config, self.base)
        else:
            raise ValueError(
                "No appropriate database model found. Please check your database_system in env_config.py"
            )
        return model
