from sqlalchemy.ext.declarative import declarative_base

from data_backend.custom_logger import CustomLogger

logging = CustomLogger("DataProcessor")


class DataProcessor:

    def __init__(self, sources, table_definitions: declarative_base()):
        self.sources = sources
        self.table_definitions = table_definitions

    def load_dfs(self):
        logging.info("Loading dataframes...")
        for source in self.sources:
            self.sources[self.sources.index(source)]['df'] = source['model'].df()

    def validate_destination_tables(self):
        logging.info("Validating destination tables...")
        for source in self.sources:
            if not self._table_exists(source['destination_table']):
                raise ValueError(
                    f"Table {source['destination_table']} does not exist! Please check your data_sources.yml file.")

    def validate_source_columns(self):
        logging.info("Validating source columns...")
        for source in self.sources:
            logging.info(f"Validating source columns for {source['name']}...")
            # Get the header columns
            columns = source['df'].columns.tolist()
            # Get the destination table columns
            table_columns = self.table_definitions.metadata.tables[source['destination_table']].columns.keys()
            # Check if all the columns in the source file are in the destination table
            if not all(elem in table_columns for elem in columns):
                raise ValueError(
                    f"Columns in {source['name']} do not match the destination table {source['destination_table']}")

    # Check if a table name exists in Base.metadata
    def _table_exists(self, table_name):
        return table_name in self.table_definitions.metadata.tables

    def process_source_column_names(self, skip: list):
        # keep only the tables that are not in the skip list
        sources = [source for source in self.sources if source['name'] not in skip]
        logging.info(
            f"Processing source column names for the source names {[source['name'] for source in sources]}...")
        for source in sources:
            # replace df column names with the destination table column names using source['column_mapping']
            self.sources[self.sources.index(source)]['df'].rename(columns=source['column_mapping'], inplace=True)
