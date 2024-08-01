import pandas as pd
import re
escape_chars = re.compile(r'[\n\t\r\f\v\\\/]')

class EXCEL_MANIPULATION():
    def __init__(self, file):
        self.file = file
        self.excel_file = pd.read_excel(file)

    def clearCol(self, col):
        self.excel_file.drop(col, axis=1, inplace=True)
        return  escape_chars.sub(" ",self.excel_file.to_json(orient='records'))
    
    def getData(self):
        return escape_chars.sub(" ",self.excel_file.to_json(orient='records'))
