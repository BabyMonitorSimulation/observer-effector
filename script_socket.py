import socketio
import requests
import asyncio


def get_token_dojot():
    url = "http://dojot.atlantico.com.br:8000/auth"
    payload = {"username": "gesad", "passwd": "temppwd"}
    headers = {"Content-Type": "application/json"}
    return requests.request("POST", url, headers=headers, json=payload).json()["jwt"]


def get_socket_token():
    url = "http://dojot.atlantico.com.br:8000/stream/socketio"
    token = get_token_dojot()
    headers = {"Authorization": f"Bearer {token}"}
    return requests.request("GET", url, headers=headers).json()['token']


token = get_socket_token()

sio = socketio.Client(logger=True, engineio_logger=True)


@sio.on('all')
def on_message(data):
    print(f'\nI received a message: {data}\n')


@sio.event
async def connect():
    print("I'm connected!")


@sio.event
def connect_error(err):
    print(err)
    print(repr(sio))

    print("\nThe connection failed!\n")
    sio.disconnect()


@sio.event
def disconnect():
    print("I'm disconnected!")


asyncio.run(
    sio.connect(f'http://dojot.atlantico.com.br:8000/?token={token}',
                transports=["websocket"], namespaces=['/all'], socketio_path='socket.io')
)

