import json

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from requests.exceptions import ConnectionError
from wtforms import IntegerField, SelectField, StringField
from wtforms.validators import DataRequired


import urllib.request
import json

class ClientDataForm(FlaskForm):
    age = StringField('Age/Возраст', validators=[DataRequired()])
    sex = StringField('Sex/Пол', validators=[DataRequired()])
    cp = StringField('Chest Pain type/Тип боли в груди', validators=[DataRequired()])
    exng = StringField('Exercise induced angina (1 = yes; 0 = no)/Стенокардия, вызванная физической нагрузкой', validators=[DataRequired()])
    trtbps = StringField('Resting blood pressure (in mm Hg)/Артериальное давление в состоянии покоя (в мм рт. ст.)', validators=[DataRequired()])
    thalachh = StringField('maximum heart rate achieved/Достигнутая максимальная частота пульса', validators=[DataRequired()])


app = Flask(__name__)
app.config.update(
    CSRF_ENABLED=True,
    SECRET_KEY='you-will-never-guess',
)

def get_prediction(age, sex, cp, exng, trtbps, thalachh):
    body = {"age": age,
            "sex": sex,
            "cp": cp,
            "exng": exng,
            "trtbps": trtbps,
            "thalachh": thalachh}

    myurl = "http://0.0.0.0:8180/predict"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    #print (jsondataasbytes)
    response = urllib.request.urlopen(req, jsondataasbytes)
    return json.loads(response.read())['predictions']

@app.route("/")
def index():
    return render_template('index.html')


@app.route('/predicted/<response>')
def predicted(response):
    response = json.loads(response)
    print(response)
    return render_template('predicted.html', response=response)


@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    form = ClientDataForm()
    data = dict()
    if request.method == 'POST':
        data["age"] = request.form.get("age")
        data["sex"] = request.form.get("sex")
        data["cp"] = request.form.get("cp")
        data["exng"] = request.form.get("exng")
        data["trtbps"] = request.form.get("trtbps")
        data["thalachh"] = request.form.get("thalachh")


        try:
            response = str(get_prediction(data["age"],
                                          data["sex"],
                                          data["cp"],
                                          data["exng"],
                                          data["trtbps"],
                                          data["thalachh"]))
            print(response)
        except ConnectionError:
            response = json.dumps({"error": "ConnectionError"})
        return redirect(url_for('predicted', response=response))
    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8181, debug=True)