from data_backend.custom_logger import CustomLogger


logging = CustomLogger("database")


class Package:
    def __init__(self, config):
        self.config = config
        self.model = None
        self.engine = None

    def create_connection(self):
        if self.config is None:
            raise ValueError("Configuration is not initialized. Call init_config() first.")

        self.model = self._get_dbs_model(self.config)
        self.engine = self.model.connect()

    def _get_dbs_model(self, config):
        if config.DATABASE_SYSTEM == "postgres":
            from package.model_postgres import PostgresModel
            model = PostgresModel(config)
        else:
            raise ValueError(
                "No appropriate database model found. Please check your database_system in config.py"
            )
        return model
    
    