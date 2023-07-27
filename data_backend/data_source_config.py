import yaml


class DataSourceConfigParser:
    XLSX_REQUIRED_FIELDS = [
        "TYPE",
        "PATH",
        "SHEET_NAME",
        "HEADER",
        "USECOLS",
        "SKIPROWS",
        "DESTINATION_TABLE"
    ]

    CSV_REQUIRED_FILES = [
        "TYPE",
        "PATH",
        "HEADER",
        "USECOLS",
        "SKIPROWS",
        "DELIMITER",
        "DESTINATION_TABLE"
    ]

    def __init__(self, file_path):
        self.config = self._load_yaml(file_path)
        self._validate_config()

    def _load_yaml(self, file_path):
        with open(file_path) as yaml_file:
            return yaml.load(yaml_file, Loader=yaml.FullLoader)

    def _validate_config(self):
        for source_name, source_config in self.config.items():
            match source_config["TYPE"]:
                case "XLSX":
                    self._validate_xlsx_config(source_config)
                case "CSV":
                    self._validate_csv_config(source_config)
                case _:
                    raise ValueError(f"Invalid source type {source_config['TYPE']}")

    def _validate_xlsx_config(self, source_config):
        for field in self.XLSX_REQUIRED_FIELDS:
            if field not in source_config:
                raise ValueError(f"Missing required field {field} in source config {source_config}")
        return True

    def _validate_csv_config(self, source_config):
        for field in self.CSV_REQUIRED_FILES:
            if field not in source_config:
                raise ValueError(f"Missing required field {field} in source config {source_config}")
        return True
