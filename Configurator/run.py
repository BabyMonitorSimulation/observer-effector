from project import app


if __name__ == "__main__":
    port = 5001
    print(f'Run Observer port:{port} \n')
    socketio.run(app, port=port)
