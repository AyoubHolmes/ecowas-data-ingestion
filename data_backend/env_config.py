import os

from dotenv import load_dotenv


class EnvConfigParser:
    REQUIRED_VARIABLES = [
        "DATABASE_SYSTEM",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
    ]

    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Read and validate configuration values
        self._validate_variables()

    def _validate_variables(self):
        for variable in self.REQUIRED_VARIABLES:
            value = self._get_env_variable(variable)
            setattr(self, variable, value)

    def _get_env_variable(self, variable_name):
        value = os.getenv(variable_name)
        if value is None:
            raise ValueError(f"Environment variable {variable_name} is not set.")
        return value
