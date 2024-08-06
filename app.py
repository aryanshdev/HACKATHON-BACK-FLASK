import flask
import os
from flask_cors import CORS
import algorithm

# Custom module imports (assuming they are custom modules)
import EXCEL_MANIPULATION
import CSV_MANIPULATION
import clean


app = flask.Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'


UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CLEANED_CSV'] = 'cleanedCSV/'

CORS(app, supports_credentials=True, origins=['http://localhost:10000'])
# Initialize session and Allow App to use it


# Define routes and logic here


@app.route('/')
def index():
    return 'Hello, World!'


@app.route('/uploadFile', methods=['POST'])
def upload_file():
    file = flask.request.files['uploadFile']
    code = flask.request.form['code']
    if (file.filename.endswith('.csv')):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],code + '.'+ file.filename.split('.')[-1]))
        clean.createDataFrame(os.path.join(app.config['UPLOAD_FOLDER'],code + '.'+ file.filename.split('.')[-1]), code)
        return flask.jsonify({"data": CSV_MANIPULATION.CSV_MANIPULATION(os.path.join(app.config['UPLOAD_FOLDER'],code + '.'+ file.filename.split('.')[-1])).getData()})
    elif (file.filename.endswith('.xlsx') or file.filename.endswith('.xls')):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],code + '.'+ file.filename.split('.')[-1]))
        clean.createDataFrame(os.path.join(app.config['UPLOAD_FOLDER'],code + '.'+ file.filename.split('.')[-1]), code)
        return flask.jsonify({"data": EXCEL_MANIPULATION.EXCEL_MANIPULATION(os.path.join(app.config['UPLOAD_FOLDER'],code + '.'+ file.filename.split('.')[-1])).getData()})


@app.route('/getDatasetDisplay', methods=['POST'])
def getDatasetDisplay():
    code = flask.request.form['code']
    if os.path.exists(os.path.join(app.config['CLEANED_CSV'], code+"_clean.csv")):
        return flask.jsonify({"data": CSV_MANIPULATION.CSV_MANIPULATION(os.path.join(app.config['CLEANED_CSV'], code+"_clean.csv")).getData()})
    else:
        return flask.jsonify({"data": "No file found"})
    
@app.route('/deleteFile', methods=['DELETE'])
def deleteFile():
    code = flask.request.form['code']
    os.remove(os.path.join(
        app.config['CLEANED_CSV'], code+"_clean.csv"))
    return ({'message': 'File deleted successfully!'})

   

# Below are the routes for the cleaning operations With Thier Maping with Clean.py Funtions


@app.route('/deleteCol', methods=['POST'])
def deleteCol():
    return 200


@app.route('/cleanColumnNames', methods=['POST'])
def cleanColumn():
    return clean.clean_column_names(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['code'])


@app.route('/dropColumn', methods=['POST'])
def dropColumn():
    return clean.drop_columns_from_string(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['col'], flask.request.form['code'])


@app.route('/removeDuplicates', methods=['POST'])
def removeDuplicates():
    return clean.remove_duplicates(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['code'])


@app.route('/checkMissing', methods=['POST'])
def checkMissing():
    return clean.check_missing_values(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv")


@app.route('/handle_NonNumeric_Fill', methods=['POST'])
def handle_NonNumeric_Fill():
    return clean.handle_nonnumeric_missing_vals_fill(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['col'], flask.request.form['code'])


@app.route('/handle_NonNumeric_Drop', methods=['POST'])
def handle_NonNumeric_Drop():
    return clean.handle_nonnumeric_missing_vals_drop(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['col'], flask.request.form['code'])


@app.route('/handle_Numeric_Missing', methods=['POST'])
def handle_NonNumeric_Missing():
    return clean.handle_numeric_missing_vals(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form["col"], flask.request.form['code'])


@app.route('/convertNumeric', methods=['POST'])
def convertNumeric():
    return clean.convert_to_numeric(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['col'], flask.request.form['code'])


@app.route('/normalizeDate', methods=['POST'])
def normalizeDate():
    return clean.normalize_date_column(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['col'], flask.request.form['code'])


@app.route('/oneHot', methods=['POST'])
def oneHot():
    return clean.one_hot_encoding(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['col'], flask.request.form['code'])


@app.route('/get_Col_Datatypes', methods=['POST'])
def get_Col_Datatypes():
    return clean.get_column_datatypes(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv")


@app.route('/drop_Rows_WO_Target', methods=['POST'])
def drop_Rows_WO_Target():
    return clean.drop_rows_without_target(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['col'], flask.request.form['code'])

# API Routes for running Differrent Algo


@app.route('/runSVM', methods=['POST'])
def runSVM():
    return algorithm.model("svm", flask.request.form['param1'], flask.request.form['param2'], flask.request.form['param3'], flask.request.form['code'],)


@app.route('/runRandomForest', methods=['POST'])
def runRandomForest():
    return algorithm.model('random_forest', flask.request.form['param1'], flask.request.form['param2'], flask.request.form['param3'], flask.request.form['code'])


@app.route('/runXGBoost', methods=['POST'])
def runXGBoost():
    return algorithm.model('xgboost', flask.request.form['param1'], flask.request.form['param2'], flask.request.form['param3'], flask.request.form['code'])


@app.route('/runDecisionTree', methods=['POST'])
def runDecisionTree():
    return algorithm.model("decision_tree", flask.request.form['param1'], flask.request.form['param2'], flask.request.form['param3'], flask.request.form['code'])


@app.route('/runBagging', methods=['POST'])
def runBagging():
    return algorithm.model('bagging', flask.request.form['param1'], flask.request.form['param2'], flask.request.form['param3'], flask.request.form['code'])


@app.route('/saveSplits', methods=['POST'])
def saveSplits():
    return algorithm.split_and_save_data(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['trainingSplits'], flask.request.form['code'])


@app.route('/setEncoder', methods=['POST'])
def setEncoder():
    return algorithm.update_encoder_status(flask.request.form['encoderStatus'], flask.request.form['code'])


@app.route('/setTarget', methods=['POST'])
def saveTarget():
    return algorithm.save_target_variable(app.config['CLEANED_CSV']+flask.request.form['code']+"_clean.csv", flask.request.form['targetValue'], flask.request.form['code'])

# FILE DDOWNLOAD SYSTEM

@app.route('/filesAvailable', methods=['POST'])
def filesAvailable():
    code = flask.request.form['code']
    response={}
    response["svm"] = os.path.join('output/', code+"_svm.pkl") if os.path.exists(os.path.join('output/', code+"_svm.pkl")) else None
    response["svm"] = os.path.join('output/', code+"_svm.pkl") if os.path.exists(os.path.join('output/', code+"_svm.pkl")) else None