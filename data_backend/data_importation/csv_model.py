import pandas as pd


class CsvModel:

    def __init__(self, config):
        self.PATH = config["PATH"]
        self.HEADER = config["HEADER"]
        self.USECOLS = config["USECOLS"]
        self.SKIPROWS = config["SKIPROWS"]
        self.DELIMITER = config["DELIMITER"]

    def df(self):
        return pd.read_csv(filepath_or_buffer=self.PATH, header=self.HEADER, usecols=self.USECOLS,
                           skiprows=self.SKIPROWS, delimiter=self.DELIMITER)
