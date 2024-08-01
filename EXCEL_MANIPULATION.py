import pandas as pd

class EXCEL_MANIPULATION():
    def __init__(self, file):
        self.file = file
        self.excel_file = pd.read_excel(file)

    def clearCol(self, col):
        self.df.drop(col, axis=1, inplace=True)
        return self.df.to_json(orient='records')
    
    def clearRow(self, row):
        self.df.drop(row, axis=0, inplace=True)
        return self.df.to_json(orient='records')