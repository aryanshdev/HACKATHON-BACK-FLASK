import flask
import EXCEL_MANIPULATION
import csv

app = flask.Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'

@app.route('/predict', methods=['POST'])
def predict():
    return 'Prediction'

@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    if(flask.request.files['file'].filename.endswith('.xlsx')): # Check if the file is an excel file
        EXCEL_MANIPULATION.EXCEL_MANIPULATION(flask.request.files['file'])
        return 'File uploaded successfully'
