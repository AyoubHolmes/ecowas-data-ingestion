from ecowas.custom_logger import CustomLogger


logging = CustomLogger("database")


class EcowasDatabase:
    def __init__(self, config):
        self.config = config
        self.model = None

    def create_connection(self):
        if self.config is None:
            raise ValueError("Configuration is not initialized. Call init_config() first.")

        self.model = self.get_model(self.config.DATABASE_SYSTEM)
        self.model = self.model(self.config)
        self.model.connect()

    def get_model(self, database_system):
        if database_system == "postgres":
            from ecowas.model_postgres import PostgresModel
            model = PostgresModel
        else:
            raise ValueError(
                "No appropriate database model found. Please check your database_system in config.py"
            )
        return model