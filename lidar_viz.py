#!/usr/bin/python
'''
Flask-powered web app for visualizing
YDLIDAR X4 data
'''
from gevent import monkey
monkey.patch_all()
import time
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import PyLidar2
import json
import logging
logging.basicConfig()

# Configure YDLIDAR X4
port = "/dev/ttyUSB0" #linux
lidar = PyLidar2.YdLidarX4(port)
if(lidar.Connect()):
    print(lidar.GetDeviceInfo())

app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
thread = None
_data = dict()

# Read LIDAR data
def getData():
  gen = lidar.StartScanning()
  data = dict(gen.next())
  lidar.StopScanning()
  return json.dumps(data)

def background_stuff():
	""" Let's do it a bit cleaner """
	while True:
		t0 = time.time()
		_data = getData()
		t = time.time()-t0
		socketio.emit('message', {'data':_data, 'time': "%.3f" % t})

@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_stuff)
        thread.start()
    return render_template('index.html')

@socketio.on('my event')
def my_event(msg):
	print msg['data']

@socketio.on('connect') # 'connect' is a pre-defined event
def on_connect():
  emit('rsp',{'status':'CONNECTED'})
@socketio.on('disconnect') # 'disconnect' is also a pre-defined event
def on_disconnect():
  print('Client disconnected')
	
if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0')
