import pandas as pd


class XlsxModel:

    def __init__(self, config):
        self.PATH = config["PATH"]
        self.SHEET_NAME = config["SHEET_NAME"]
        self.HEADER = config["HEADER"]
        self.USECOLS = config["USECOLS"]

    def df(self, nrows=None):
        return pd.read_excel(io=self.PATH, sheet_name=self.SHEET_NAME, header=self.HEADER,
                             usecols=self.USECOLS, engine='openpyxl', nrows=nrows)
