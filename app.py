import random, os
from flask import Flask, render_template, redirect, url_for, send_from_directory
app = Flask(__name__)


def envd(path):
    if 'UP_STAGE' in os.environ:
        env = os.environ['UP_STAGE']
        return "/" + env + path
    else:
        return path

@app.route("/", methods=['GET'])
def get_index():
    return redirect(envd(url_for('get_run_clip', run_id=1, clip_id=1)))


@app.route("/clips/<clip_filename>", methods=['GET'])
def get_clip(clip_filename):
    return send_from_directory('clips', clip_filename)


@app.route("/runs/<run_id>/clips/<clip_id>", methods=['GET'])
def get_run_clip(run_id, clip_id):
    clip_filename = str(random.randrange(1, 3)) + '.mp3'
    clip_url = envd(url_for('get_clip', clip_filename=clip_filename))
    bah_result_url = envd(url_for('post_run_clip_result', run_id=run_id, clip_id=clip_id, result='bah'))
    dah_result_url = envd(url_for('post_run_clip_result', run_id=run_id, clip_id=clip_id, result='dah'))
    return render_template('index.html', bah_result_url=bah_result_url, dah_result_url=dah_result_url, clip_url=clip_url, clip_id=clip_id)


@app.route("/runs/<run_id>/clips/<clip_id>/<result>", methods=['POST'])
def post_run_clip_result(run_id, clip_id, result):
    next_clip_id = int(clip_id) + 1
    return redirect(envd(url_for('get_run_clip', run_id=run_id, clip_id=next_clip_id)))
