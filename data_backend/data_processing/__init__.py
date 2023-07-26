import pandas as pd


class DataProcessor:
    def __init__(self, file_path, model):
        self.file_path = file_path
        self.file_extension = self.get_file_extension()
        self.df = None
        self.model = model

    def get_file_extension(self):
        return self.file_path.split(".")[-1]

    def load_file(self):
        if self.file_extension == "csv":
            self.df = pd.read_csv(self.file_path)
        elif self.file_extension == "xlsx":
            self.df = pd.read_excel(self.file_path)
        else:
            raise ValueError("File extension not supported")

    def add_timestamp(self):
        self.df['date'] = pd.Timestamp.now().strftime('%Y-%m-%d')
