import flask
from flask_session import Session 
import os
from flask_cors import CORS

# Custom module imports (assuming they are custom modules)
import EXCEL_MANIPULATION
import CSV_MANIPULATION 
import clean


app = flask.Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'AVENGEAI-FLASK-SESSION'
Session(app)

UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app, origins=['http://localhost:5173'])  
# Initialize session and Allow App to use it
Session(app)

# Define routes and logic here
@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/uploadFile', methods=['POST'])
def upload_file():
    file = flask.request.files['uploadFile']
    print(file.filename)
    if(file.filename.endswith('.csv')):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flask.session["current"] = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        return CSV_MANIPULATION.CSV_MANIPULATION(flask.session["current"]).getData(),200;
    elif(file.filename.endswith('.xlsx')):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flask.session["current"] = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        return EXCEL_MANIPULATION.EXCEL_MANIPULATION(flask.session["current"]).getData(),200;
    

@app.route('/deleteCol', methods=['POST'])
def deleteCol():
    if(flask.session['current']):
        return flask.session['current'].clearCol(flask.request.form['col'])
    else:
        return ({'message': 'No file uploaded yet!'})

@app.route('/deleteFile', methods=['DELETE'])
def deleteFile():
    print(flask.session)
    if(flask.session.get('current')):
        os.remove(flask.session.get('current'))
        flask.session.pop('current', None)
        return ({'message': 'File deleted successfully!'})

    else:
        return ({'message': 'No file uploaded yet!'})
    
# Below are the routes for the cleaning operations With Thier Maping with Clean.py Funtions
    
@app.route('/cleanColumn', methods=['POST'])
def cleanColumn():
    return clean.clean_column_names(flask.session.get('current'))

@app.route('/dropColumn', methods=['POST'])
def dropColumn():
    return clean.drop_columns_from_string(flask.session.get("current"),flask.request.form['col'])

@app.route('/removeDuplicates', methods=['POST'])
def removeDuplicates():
    return clean.remove_duplicates(flask.session.get("current"))

@app.route('/checkMissing', methods=['POST'])
def checkMissing():
    return clean.check_missing_values(flask.session.get("current"))

@app.route('/handle_NonNumeric_Fill', methods=['POST'])
def handle_NonNumeric_Fill():
    return clean.handle_nonnumeric_missing_vals_fill(flask.session.get("current"), flask.request.form['col'])

@app.route('/handle_NonNumeric_Drop', methods=['POST'])
def handle_NonNumeric_Drop():
    return clean.handle_nonnumeric_missing_vals_drop(flask.session.get("current"), flask.request.form['col'])

@app.route('/handle_NonNumeric_Missing', methods=['POST'])
def handle_NonNumeric_Missing():
    return clean.handle_numeric_missing_vals(flask.session.get("current"))

@app.route('/handle_Numeric_Missing', methods=['POST'])
def handle_NonNumeric_Missing():
    return clean.handle_numeric_missing_vals(flask.session.get("current"))

@app.route('/convertNumeric', methods=['POST'])
def convertNumeric():
    return clean.convert_to_numeric(flask.session.get("current"), flask.request.form['col'])

@app.route('/normalizeDate', methods=['POST'])
def normalizeDate():
    return clean.normalize_date_column(flask.session.get("current"), flask.request.form['col'])

@app.route('/oneHot', methods=['POST'])
def oneHot():
    return clean.one_hot_encoding(flask.session.get("current"), flask.request.form['col'])

@app.route('/get_Col_Datatypes', methods=['POST'])
def get_Col_Datatypes():
    return clean.get_column_datatypes(flask.session.get("current"))

@app.route('/drop_Rows_WO_Target', methods=['POST'])
def drop_Rows_WO_Target():
    return clean.drop_rows_without_target(flask.session.get("current"), flask.request.form['col'])