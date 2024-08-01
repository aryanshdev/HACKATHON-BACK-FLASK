import pandas as pd  # IMPORT


class CSV_MANIPULATION():
    def __init__(self , file):
        self.file = file
        self.csv_file = pd.read_csv(file)

    def clearCol(self, col):
        self.csv_file.drop(columns=[col], inplace=True)
        return self.csv_file.to_json(orient='records')

    def getData(self):
        return self.csv_file.to_json(orient='records')

    def changeColumnValues(self, col, new_value):
        self.csv_file[col] = new_value
        return self.csv_file.to_json(orient='records')
