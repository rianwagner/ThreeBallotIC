from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('connect', namespace='/serverA')
def handle_serverA_connect():
    print('Cliente conectado a serverA')
    socketio.emit('message_from_serverA_to_serverB',
                  'Mensagem de serverA', namespace='/serverB')


if __name__ == '__main__':
    socketio.run(app, debug=True, ssl_context=(
        'server.crt', 'server.key'), port=5000)
