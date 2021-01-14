import argparse
from flask import Flask, jsonify, request, send_from_directory
from flask import redirect, url_for
from flask import render_template
import joblib
import socket
import json
import numpy as np
import pandas as pd
import os,re

## import model specific functions and variables
from model.model import model_train, model_load, model_predict
from model.model import MODEL_VERSION, MODEL_VERSION_NOTE

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
LOGS_DIR = os.path.join(THIS_DIR, "logfiles")
HOST = "127.0.0.1"
PORT = 8080
app = Flask(__name__)

@app.route('/logfiles/<path:path>', methods=['GET'])
def send_js(path):
    return send_from_directory(LOGS_DIR, path)

@app.route("/")
def landing():
    return render_template('index.html')
 
@app.route("/index")
def index():
    return render_template('index.html')
    
@app.before_first_request
def startup():
    global global_data, global_models
    print(".. loading models")
    global_data,global_models = model_load(training=False)
    print(".. all models loaded") 
    return redirect(url_for('landing'))

@app.route("/logs", methods=['GET', 'POST'])
def logs():
    return render_template('logs.html')

@app.route("/logslist", methods=['GET', 'POST'])
def logslist():
    files = [f for f in os.listdir(LOGS_DIR)]
    return jsonify(files)

@app.route('/predict', methods=['GET','POST'])
def predict():
    """
    basic predict function for the API
    """
    
    if not request.json:
        print("ERROR: API (predict): did not receive request data")
        return jsonify([]), 400
    
    ## input checking
    if 'country' not in request.json:
        print("WARNING API (predict): received request, but no country specified, assuming 'all'")
        country = 'all'
    else:
        country = request.json['country']
    
    if 'target_date' not in request.json:
        print("ERROR API (predict): received request, but no 'target_date' found within")
        return jsonify([]), 400
           
    target_date = request.json['target_date']
    
    if target_date is None:
        print("ERROR API (predict): received request, but no 'target_date' found within")
        return jsonify([]), 400
    
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', target_date)
    try:
        year, month, day = m.group(1, 2, 3)
    except:
        print("ERROR API (predict): 'target_date' format is invalid")
        return jsonify([]), 400
        
    result = {}
    try:
        _result = model_predict(country,year,month,day,all_models=global_models,all_data=global_data)
        ## convert numpy objects so ensure they are serializable
        for key,item in _result.items():
            if isinstance(item,np.ndarray):
                result[key] = item.tolist()
            else:
                result[key] = item
        return(jsonify(result))
    except Exception as e:
        print("ERROR API (predict): model_predict returned: {}".format(str(e)))
        return jsonify([]), 400

@app.route('/train', methods=['GET','POST'])
def train():
    """
    basic predict function for the API

    the 'mode' give you the ability to toggle between a test version and a production verion of training
    """
    
    test = False
    if 'mode' in request.json:
        if request.json['mode'] == 'test':
            test = True

    print("... training model")
    data_dir = os.path.join(THIS_DIR,"data","cs-train")
    try:
        model_train(data_dir,test=test)
        print("... training complete")
        # reload models and data after re-train
        print("... reloading models in cache")
        global_data,global_models = model_load(training=False)
        return(jsonify(True))
    except Exception as e:
        print("ERROR API (train): model_train returned: {}".format(str(e)))
        return jsonify([]), 400
        
    
if __name__ == '__main__':


    ## parse arguments for debug mode
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", action="store_true", help="debug flask")
    args = vars(ap.parse_args())

    if args["debug"]:
        app.run(debug=True, port=PORT)
    else:
        app.run(host=HOST, threaded=True ,port=PORT)

