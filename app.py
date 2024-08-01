import flask
from flask_session import Session 
import os

# Custom module imports (assuming they are custom modules)
import EXCEL_MANIPULATION
import CSV_MANIPULATION 


app = flask.Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'AVENGEAI-FLASK-SESSION'
Session(app)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize the flask.session
Session(app)

# Define routes and logic here
@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/uploadFile', methods=['POST'])
def upload_file():
    file = flask.request.files['uploadFile']
    if(file.filename.endswith('.csv')):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flask.session["current"] = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        return CSV_MANIPULATION.CSV_MANIPULATION(flask.session["current"]).getData();
    elif(file.filename.endswith('.xlsx')):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flask.session["current"] = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        return EXCEL_MANIPULATION.EXCEL_MANIPULATION(flask.session["current"]).getData();
    

@app.route('/deleteCol', methods=['POST'])
def deleteCol():
    if(flask.session['current']):
        return flask.session['current'].clearCol(flask.request.form['col'])
    else:
        return ({'message': 'No file uploaded yet!'})
