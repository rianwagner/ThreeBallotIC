from flask import Flask, render_template
from flask_socketio import SocketIO

import socketio as socketzin
import requests

# app = Flask(__name__, static_folder='static')
# socketio = SocketIO(app, cors_allowed_origins="*")

sio = socketzin.Client(ssl_verify=False)


@sio.event(namespace="/serverC")
def connect():
    print("conectado")


if __name__ == '__main__':
    sio.connect("https://127.0.0.1:5002")
    sio.wait()
    # socketio.run(app, debug=True, ssl_context=(
    #    'server.crt', 'server.key'), port=5001)
