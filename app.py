import flask
from flask_session import Session 
import os
from flask_cors import CORS
import uuid

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
app.config['INTERMEDIATE_FOLDER'] = 'intermediates/'

CORS(app,supports_credentials=True, origins=['http://localhost:5173'])  
# Initialize session and Allow App to use it
Session(app)

# Define routes and logic here
@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/uploadFile', methods=['POST'])
def upload_file():
    file = flask.request.files['uploadFile']
    code = flask.request.form['code']
    if(file.filename.endswith('.csv')):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flask.session["current"] = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        clean.createDataFrame(flask.session.get("current"),code)
        flask.session["currentClean"] = os.path.join(app.config['INTERMEDIATE_FOLDER'], code+"_clean.csv")
        return {"data":CSV_MANIPULATION.CSV_MANIPULATION(flask.session["current"]).getData(), "code": code}
    elif(file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        flask.session["current"] = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        clean.createDataFrame(flask.session.get("current"),code)
        flask.session["currentClean"] = os.path.join(app.config['INTERMEDIATE_FOLDER'], code+"_clean.csv")
        print(os.path.join(app.config['INTERMEDIATE_FOLDER'], code+"_clean.csv"))
        print(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv")
        return {"data":EXCEL_MANIPULATION.EXCEL_MANIPULATION(flask.session["current"]).getData(), "code": code}
    


@app.route('/deleteFile', methods=['DELETE'])
def deleteFile():
    code = flask.request.form['code']
    if(flask.session.get('current')):
        os.remove(flask.session.get('current'))
        os.remove(os.path.join(app.config['INTERMEDIATE_FOLDER'], code+"_clean.csv"))
        return ({'message': 'File deleted successfully!'})

    else:
        return ({'message': 'No file uploaded yet!'})
    
# Below are the routes for the cleaning operations With Thier Maping with Clean.py Funtions
    
@app.route('/deleteCol', methods=['POST'])
def deleteCol():
    if(flask.session['current']):
        return flask.session['current'].clearCol(flask.request.form['col'])
    else:
        return ({'message': 'No file uploaded yet!'})


@app.route('/cleanColumnNames', methods=['POST'])
def cleanColumn():
    return clean.clean_column_names(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv",flask.request.form['code'])

@app.route('/dropColumn', methods=['POST'])
def dropColumn():
    return clean.drop_columns_from_string(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv",flask.request.form['col'],flask.request.form['code'])

@app.route('/removeDuplicates', methods=['POST'])
def removeDuplicates():
    return clean.remove_duplicates(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv",flask.request.form['code'])

@app.route('/checkMissing', methods=['POST'])
def checkMissing():
    return clean.check_missing_values(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv")

@app.route('/handle_NonNumeric_Fill', methods=['POST'])
def handle_NonNumeric_Fill():
    return clean.handle_nonnumeric_missing_vals_fill(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv", flask.request.form['col'],flask.request.form['code'])

@app.route('/handle_NonNumeric_Drop', methods=['POST'])
def handle_NonNumeric_Drop():
    return clean.handle_nonnumeric_missing_vals_drop(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv", flask.request.form['col'],flask.request.form['code'])

@app.route('/handle_Numeric_Missing', methods=['POST'])
def handle_NonNumeric_Missing():
    return clean.handle_numeric_missing_vals(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv",flask.request.form['code'])

@app.route('/convertNumeric', methods=['POST'])
def convertNumeric():
    return clean.convert_to_numeric(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv", flask.request.form['col'],flask.request.form['code'])

@app.route('/normalizeDate', methods=['POST'])
def normalizeDate():
    return clean.normalize_date_column(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv", flask.request.form['col'],flask.request.form['code'])

@app.route('/oneHot', methods=['POST'])
def oneHot():
    return clean.one_hot_encoding(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv", flask.request.form['col'],flask.request.form['code'])

@app.route('/get_Col_Datatypes', methods=['POST'])
def get_Col_Datatypes():
    return clean.get_column_datatypes(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv")

@app.route('/drop_Rows_WO_Target', methods=['POST'])
def drop_Rows_WO_Target():
    return clean.drop_rows_without_target(app.config['INTERMEDIATE_FOLDER']+flask.request.form['code']+"_clean.csv", flask.request.form['col'],flask.request.form['code'])