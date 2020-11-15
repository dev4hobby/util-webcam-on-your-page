#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, request, render_template, Response

Camera = import_module('camera_opencv').Camera
app = Flask(__name__)

mem_order = [
  'textbox',
  'check1',
  'check2',
  'check3',
  'range1',
  'drop1',
  'radio1',
  'radio2',
  'radio3',
]
membox = {
  'textbox':0,
  'check1':0,
  'check2':0,
  'check3':0,
  'range1':0,
  'drop1':0,
  'radio1':0,
  'radio2':0,
  'radio3':0,
}

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/setting')
def setting():
    return render_template('setting.html', membox=membox)

@app.route('/setting_post', methods=['POST','GET'])
def setting_post():
    if request.method == 'POST':
        result = request.form

    try:
        for x in mem_order:
            membox[x] = result.get(x)
            print(result.get(x))
    except Exception as e:
        print (e)

    return render_template('setting_post.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
