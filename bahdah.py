import random
from flask import Flask, render_template, redirect, url_for, send_from_directory
app = Flask(__name__)


@app.route("/clips/<clip_filename>", methods=['GET'])
def get_clip(clip_filename):
    return send_from_directory('clips', clip_filename)


@app.route("/runs/<run_id>/clips/<clip_id>", methods=['GET'])
def get_run_clip(run_id, clip_id):
    clip_filename = str(random.randrange(1, 3)) + '.mp3'
    return render_template('index.html', run_id=run_id, clip_id=clip_id, clip_filename=clip_filename)


@app.route("/runs/<run_id>/clips/<clip_id>/<result>", methods=['POST'])
def post_run_clip_result(run_id, clip_id, result):
    next_clip_id = int(clip_id) + 1
    return redirect(url_for('get_run_clip', run_id=run_id, clip_id=next_clip_id))
