from server import server_app, socketio

app = server_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
