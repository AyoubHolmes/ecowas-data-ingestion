from data_backend.data_importation import DataImportation
from data_backend.data_processing import DataProcessor
from data_backend.data_source_config import DataSourceConfigParser
from data_backend.database import Database
from data_backend.database.table_definitions import Base, KpiValue, Kpi, Country
from data_backend.database.tasks import Tasks
from data_backend.env_config import EnvConfigParser


def main():
    # Initialize the config
    env = EnvConfigParser()

    # Initialize the Database destination
    db = Database(env, table_definitions=Base)
    db.create_connection()

    data_source_file_name = "data_sources.yml"
    data_source = DataSourceConfigParser(data_source_file_name)

    # Initialize the data importation, Extraction Phase
    data_importation = DataImportation(data_source.config)
    data_importation.load_data_sources()

    # Initialize the data processing, Transformation Phase
    data_processed = DataProcessor(data_importation.sources, table_definitions=Base)
    data_processed.load_dfs()  # Load the dataframes Country, Kpi, KpiValue
    data_processed.validate_destination_tables()
    data_processed.process_source_column_names(skip=["country", "kpi"])
    data_processed.validate_source_columns()

    # Initialse the tasks
    tasks = Tasks(db.model)
    tasks.initialize_tables(tables=[KpiValue, Kpi, Country])  # Keep the order

    country = [source for source in data_processed.sources if source['name'] == "country"][0]
    kpi = [source for source in data_processed.sources if source['name'] == "kpi"][0]
    kpi_values = [source for source in data_processed.sources if source['name'] == "kpi_value"][0]

    tasks.to_sql(country['destination_table'], country['df'], if_exists="append")
    tasks.to_sql(kpi['destination_table'], kpi['df'], if_exists="append")
    kpi_values['df'] = tasks.process_new_values_for_kpi_value(kpi_values)
    tasks.to_sql(kpi_values['destination_table'], kpi_values['df'], if_exists="append", index=True, index_label="id")


if __name__ == "__main__":
    main()
