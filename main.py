from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room, rooms

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def main():
    return render_template('index.html')


@socketio.on('my_event')
def handle_message(data):
    print('conected : ' + str(data['author']))
    join_room(data['room'])
    emit('sistem_msg', {'msg': f"{data['author']} присоеденился к чату"}, room=data['room'])


@socketio.on('send_msg')
def handle_msgs(data):
    print(f"new msg from {data['author']} : {data['text']}")
    emit('new_msg', data, room=data['room'])


@socketio.on('close')
def handle_message(data):
    print('disconnected : ' + str(data['author']))
    print(rooms())
    emit('sistem_msg', {'msg': f"{data['author']} покинул чат"}, room=data['room'])


if __name__ == '__main__':
    print("starting server...")
    socketio.run(app, host='0.0.0.0', port=81)
