from data_backend.custom_logger import CustomLogger

logging = CustomLogger("DataImportation")


class DataImportation:
    def __init__(self, config):
        self.config = config
        self.sources = []

    def load_data_sources(self):
        for source_name, source_config in self.config.items():
            logging.info(f"Loading source {source_name}")
            source_model = self._get_source_model(source_config)
            self.sources.append({
                "name": source_name,
                "model": source_model,
                "destination_table": source_config["DESTINATION_TABLE"],
                "column_mapping": source_config["COLUMN_MAPPING"]
            })

    def _get_source_model(self, source_config):
        match source_config["TYPE"]:
            case "XLSX":
                from data_backend.data_importation.xlsx_model import XlsxModel
                return XlsxModel(source_config)
            case "CSV":
                from data_backend.data_importation.csv_model import CsvModel
                return CsvModel(source_config)
            case _:
                raise ValueError(f"Invalid source type {source_config['TYPE']}")
