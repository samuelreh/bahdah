import random, os, datetime
from random import *
from flask import Flask, render_template, redirect, url_for, send_from_directory, request, session
import pyrebase

app = Flask(__name__)
app.secret_key = 'super secret key'

config = {
  "apiKey": "AIzaSyCyMYbU4swN-cSYyV7KefYyLuEf0G2bsMg",
  "authDomain": "",
  "databaseURL": "https://bahdah-1.firebaseio.com",
  "storageBucket":""
  # "serviceAccount": "./bahdah-1-firebase-adminsdk-naxmt-0eae5a615f.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def envd(path):
    if 'UP_STAGE' in os.environ:
        env = os.environ['UP_STAGE']
        return "/" + env + path
    else:
        return path

@app.route("/", methods=['GET'])
def get_index():
    trial_url = envd(url_for('create_trial'))
    return render_template('index.html', trial_url=trial_url)


@app.route("/trials", methods=['POST'])
def create_trial():
    files = os.listdir('clips') * 3
    shuffle(files)
    session['files'] = files
    session['name'] = request.form['name']
    return redirect(envd(url_for('get_event', event_id=0)))


@app.route("/files/<filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory('clips', filename)


@app.route("/events/<event_id>", methods=['GET'])
def get_event(event_id):
    if int(event_id) >= len(session['files']):
        return redirect(envd(url_for('get_fin')))
    filename = session['files'][int(event_id)]
    file_url = envd(url_for('get_file', filename=filename))
    result_url = envd(url_for('create_result'))
    total = (len(session['files']) - 1)
    return render_template('event.html', result_url=result_url, event_id=event_id, file_url=file_url, total=total, filename=filename)

@app.route("/fin", methods=['GET'])
def get_fin():
    return render_template('fin.html')


@app.route("/results", methods=['POST'])
def create_result():
    name = session["name"]
    event_id = request.form["event_id"]
    data = request.form.to_dict()
    data["ip"] = get_ip()
    data["time"] = datetime.datetime.now().isoformat()
    db.child("subjects").child(name).child("results").child(event_id).set(data)
    return redirect(envd(url_for('get_event', event_id=int(event_id) + 1)))

def get_ip():
    if request.headers.getlist("X-Forwarded-For"):
       return request.headers.getlist("X-Forwarded-For")[0]
    else:
       return request.remote_addr
