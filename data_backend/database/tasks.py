from data_backend.custom_logger import CustomLogger

logging = CustomLogger("TASKS")


class Tasks:
    def __init__(self, db):
        self.db = db

    def initialize_tables(self, tables):
        # create table if not exists
        try:
            self.db.re_create_table(tables=tables)
        except Exception as e:
            logging.error(e)
            exit(1)
        finally:
            logging.info("Initialized tables successfully!")

    def to_sql(self, destination_table, df, if_exists="append", index=False, index_label=None):
        try:
            df.to_sql(destination_table, self.db.engine, if_exists=if_exists, index=index, index_label=index_label)
        except Exception as e:
            logging.error(e)
        finally:
            logging.info(f"Loaded data for {destination_table} successfully!")

    def process_new_values_for_kpi_value(self, source):
        df = source['df']
        # process country_id e.g. Check if the country exists in the country table and replace by its id
        df['country_id'] = df['country_id'].apply(self._get_country_id)
        # Convert the 'country_id' column to integer data type
        df['country_id'] = df['country_id'].astype('Int64')

        # process kpi_id e.g. Check if the kpi exists in the kpi table and replace by its id
        df['kpi_id'] = df['kpi_id'].apply(self._get_kpi_id)
        # Convert the 'kpi_id' column to integer data type
        df['kpi_id'] = df['kpi_id'].astype('Int64')
        return df

    def _get_country_id(self, country_name):
        country = self.db.base.metadata.tables['country']
        # get the value and cast to int it's the table id
        res = self.db.get_one(table_cls=country, select_column='id', where_column='label', where_value=country_name)
        return int(res) if res is not None else None

    def _get_kpi_id(self, kpi_name):
        kpi = self.db.base.metadata.tables['kpi']
        # get the value and cast to int it's the table id
        res = self.db.get_one(table_cls=kpi, select_column='id', where_column='label', where_value=kpi_name)
        return res

    def distinct_values(self, source):
        df = source['df']
        df = df.drop_duplicates()
        return df
