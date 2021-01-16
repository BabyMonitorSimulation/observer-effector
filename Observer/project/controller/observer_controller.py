from project.entity.observer_broker import ObserverBroker
from flask import jsonify, request
from project import app
from time import sleep
import socketio
import requests
import json


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/start", methods=["POST"])
def start():
    ObserverBroker(request.json).start()
    print("Start OK")
    return jsonify({"msg": "ok"})


# def get_token_dojot():
#     url = "http://dojot.atlantico.com.br:8000/auth"
#     payload = {"username": "gesad", "passwd": "temppwd"}
#     headers = {"Content-Type": "application/json"}
#     return requests.request("POST", url, headers=headers, json=payload).json()["jwt"]
        
# def get_socket_token():
#     url = "http://dojot.atlantico.com.br:8000/stream/socketio"
#     token = get_token_dojot()
#     headers = {"Authorization": f"Bearer {token}"}
#     return requests.request("GET", url, headers=headers).json()['token']

# socketio = socketio.Client(logger=True, engineio_logger=True)


# @socketio.event
# def connect():
#     print("connection established")


# @socketio.event(namespace="/all")
# def my_message(data):
#     print("message received with ", data)
#     socketio.emit("my response", {"response": "my response"})


# @socketio.event
# def disconnect():
#     print("disconnected from server")


# token = get_socket_token()
# headers={'token':token}
# socketio.connect(f'http://dojot.atlantico.com.br:8000?token={token}', transports=["websocket"])
# # JS -> io.connect("http://dojot.atlantico.com.br:8000/", { 'query': token, 'transports': ['websocket'] })

# socketio.wait()
