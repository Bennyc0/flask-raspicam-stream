from flask import Flask, render_template, Response, redirect, url_for
from rpi_camera import RPiCamera
from datetime import datetime

app = Flask(__name__)
picam = RPiCamera()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/stream')
def stream():
    return render_template("stream.html")

#the generator, a special type of function that yields, instead of returns.
def gen(camera):
    while True:
        frame = camera.get_frame()

        # Each frame is set as a jpg content type. Frame data is in bytes.
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/get-livestream')
def get_livestream():
    feed = Response(gen(picam), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    print(type(feed))
    return feed


@app.route('/record')
def record():
    return render_template('record.html')


@app.route('/start-recording')
def start_recordng():
    time = datetime.now().strftime("%m/%d/%Y_%H:%M:%S")
    video = "static/videos/"+ time +".h264"

    picam.resolution = (640, 480)
    picam.start(video)
    return redirect(url_for('record'))


@app.route('/stop-recording')
def stop_recording():
    picam.stop()
    return redirect(url_for('record'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True )
