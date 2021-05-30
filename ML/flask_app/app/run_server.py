# USAGE
# Start the server:
# 	python run_front_server.py
# Submit a request via Python:
#	python simple_request.py

# import the necessary packages
import dill
import pandas as pd
import os
dill._dill._reverse_typemap['ClassType'] = type
#import cloudpickle
import flask
import logging
from logging.handlers import RotatingFileHandler
from time import strftime

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

def load_model(model_path):
    # load the pre-trained model
    global model
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    print(model)

modelpath = "/app/app/models/cb_pipeline.dill"
load_model(modelpath)

@app.route("/", methods=["GET"])
def general():
    return """Welcome to heart attack analysis prediction process. Please use 'http://<address>/predict' to POST"""

@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}
    dt = strftime("[%Y-%b-%d %H:%M:%S]")
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":

        age, sex, cp, exng, trtbps, thalachh = 0, 0, 0, 0, 0, 0
        request_json = flask.request.get_json()
        if request_json["age"]:
            age = request_json["age"]

        if request_json["sex"]:
            sex = request_json["sex"]

        if request_json["cp"]:
            cp = request_json["cp"]

        if request_json["exng"]:
            exng = request_json["exng"]

        if request_json["trtbps"]:
            trtbps = request_json["trtbps"]

        if request_json["thalachh"]:
            thalachh = request_json['thalachh']
        logger.info(f'{dt} Data: age={age}, sex={sex}, cp={cp}, '
                    f'exng={exng}, trtbps={trtbps}, thalachh={thalachh}')
        try:
            preds = model.predict_proba(pd.DataFrame({"age": [age],
                                                  "sex": [sex],
                                                  "cp": [cp],
                                                      "exng": [exng],
                                                      "trtbps": [trtbps],
                                                      "thalachh": [thalachh]
                                                      }))
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = preds[:, 1][0]
        # indicate that the request was a success
        data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
        "please wait until server has fully started"))
    port = int(os.environ.get('PORT', 8180))
    app.run(host='0.0.0.0', debug=True, port=port)