import pandas as pd

class EXCEL_MANIPULATION():
    def __init__(self, file):
        self.file = file
        self.excel_file = pd.read_excel(file)

    def clearCol(self, col):
        self.excel_file.drop(col, axis=1, inplace=True)
        return self.excel_file.to_json(orient='records')
    
    def getData(self):
        return self.excel_file.to_json(orient='records')