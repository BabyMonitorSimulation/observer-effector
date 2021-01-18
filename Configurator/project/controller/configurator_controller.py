from project import app
from flask import jsonify, request
from time import sleep
import requests


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/", methods=["POST"])
def start():

    if request.json["interface_type"] == "broker":
        config_observer = data_config_observer(request.json)
        config_effector = data_config_effector(request.json)
        requests.post("http://localhost:4001/start", json=config_observer)
        requests.post("http://localhost:4002/configure", json=config_effector)


    if request.json["interface_type"] == "middleware":
        config_observer = data_config_observer(request.json)
        config_effector = data_config_effector(request.json)
        requests.post("http://localhost:4001/start", json=config_observer)
        requests.post("http://localhost:4002/configure", json=config_effector)

    return jsonify({"msg": "ok"})


def data_config_observer(request_json: dict):
    return {
        "interface_type": request_json["interface_type"],
        "connection_config": request_json["connection_config"],
        "normal_scenario": request_json["normal_scenario"],
        "exceptional_scenario": request_json["exceptional_scenario"],
    }


def data_config_effector(request_json: dict):
    return {
        "adaptation_actions": request_json["adaptation_actions"],
        "return_to_normal_actions": request_json["return_to_normal_actions"],
    }
