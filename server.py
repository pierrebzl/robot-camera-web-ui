from flask import Flask, render_template, request, jsonify, Response, make_response, send_file
from camera import Camera
import datetime
import time

import sys
from importlib import import_module

env = sys.argv[1] if len(sys.argv) == 2 else 'default'
config = import_module('conf.%s' % env).config

# Time zone relative to UTC
TZ = -4 * 3600

app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; '
                                            'boundary=frame')


@app.route('/forward')
def forward():
    app.q.put(('forward', config['STEP_DELAY']))
    return jsonify({})


@app.route('/stop')
def stop():
    app.q.put(('stop',))
    return jsonify({})


@app.route('/backward')
def backward():
    app.q.put(('backward', config['STEP_DELAY']))
    return jsonify({})


@app.route('/take_pic')
def take_pic():
    st = datetime.datetime.fromtimestamp(time.time() + TZ).strftime('%Y-%m-%d %H:%M:%S')
    pic = take_pic(Camera())
    _file = app.static_folder + "/" + st + ".jpg"
    with open(_file, "wb") as fh:
        fh.write(pic)
        fh.close()
    return st + ".jpg"


@app.route('/record_vid')
def record_vid():
    print("record_vid")
    # app.q.put(('record_vid',))
    return jsonify({})


def take_pic(camera):
    return camera.get_frame()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def setup(q):
    app.q = q
    return app
