# Flask Imports 
from flask import Flask, session, request
from flask_session import Session 
# Manipulation Imports
import EXCEL_MANIPULATION, CSV_MANIPULATION 


# SESSION LIKE EXPRESS_SESSION,
# IT HELPS TO SEPRATE USERS SESSIONS
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem' 
app.secret_key = 'AVENGEAI-FLASK-SESSION'
Session(app)    

@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'

@app.route('/predict', methods=['POST'])
def predict():
    return 'Prediction'

@app.route('/uploadFile', methods=['POST'])
def uploadFile():
    file = request.files['file']
    if(file.filename.endswith('.xlsx') or file.filename.endswith('.xls')): # Check if the file is an excel file
        openedFile =  EXCEL_MANIPULATION.EXCEL_MANIPULATION(file)
        return ({'message': 'File uploaded successfully!' , "data" : openedFile.getData()})
    elif(file.filename.endswith('.csv')):
        openedFile =  CSV_MANIPULATION.CSV_MANIPULATION(file)
        return ({'message': 'File uploaded successfully!' , "data" : openedFile.getData()})
    else:
        return ({'message': 'Invalid file format!'}), 400

@app.route('/deleteCol', methods=['POST'])
def deleteCol():
    if(session['current']):
        return session['current'].clearCol(request.form['col'])
    else:
        return ({'message': 'No file uploaded yet!'})
