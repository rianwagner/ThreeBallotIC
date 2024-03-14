from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect', namespace='/serverC')
def handle_serverC_connect():
    print('Cliente conectado a serverC')


@socketio.on('message_from_serverB_to_serverC', namespace='/serverC')
def handle_message_from_serverB(message):
    print('Mensagem de serverB recebida em serverC:', message)


if __name__ == '__main__':
    socketio.run(app, debug=True, ssl_context=(
        'server.crt', 'server.key'), port=5002)
