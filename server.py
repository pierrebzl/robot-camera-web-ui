from flask import Flask, render_template, request, jsonify, Response
#from camera import Camera
#import robot

app = Flask(__name__, template_folder='./templates')

@app.route('/')
def index():
	return render_template('index.html')

def gen(camera):
    while True:
    #    frame = camera.get_frame()
    #    yield (b'--frame\r\n'
    #           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    	print "while"

@app.route('/Avancer')
def test():
	print "jojo est un bg"
	return "True"

@app.route('/Reculer')
def tet():
	#robot.toggleBuzzer()
	return "True"

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
        mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
	app.run(debug=True, port=8080, host= '0.0.0.0')

