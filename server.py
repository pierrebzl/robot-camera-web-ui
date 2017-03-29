from flask import Flask, render_template, request, jsonify, Response
from camera import Camera
# import robot

app = Flask(__name__, template_folder='./templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; '
                                            'boundary=frame')


@app.route('/forward')
def forward():
    print("fw")
    app.q.put(('forward',))
    return jsonify({})


@app.route('/stop')
def stop():
    print("stop")
    app.q.put(('stop',))
    return jsonify({})


@app.route('/backward')
def backward():
    print("bw")
    app.q.put(('backward',))
    return jsonify({})


@app.route('/take_pic')
def take_pic():
    print("take_pic")
    app.q.put(('take_pic',))
    return jsonify({})


@app.route('/record_vid')
def record_vid():
    print("record_vid")
    app.q.put(('record_vid',))
    return jsonify({})


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def setup(q):
    app.q = q
    return app
