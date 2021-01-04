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
        config_decider = data_config_decider(request.json)
        requests.post("http://localhost:5001/start", json=config_observer)
        # requests.post("http://localhost:5002/", json=config_decider)

    if request.json["interface_type"] == "middleware":
        pass

    return jsonify({"msg": "ok"})


def data_config_observer(request_json: dict):
    return {
            "config_broker": request_json["config_broker"],
            "exceptional_scenario": request_json["exceptional_scenario"],
           }

def data_config_decider(request_json: dict):
    return {
            "steps_to_adapt": request_json["steps_to_adapt"],
            "steps_for_behave_normal": request_json["steps_for_behave_normal"],
           }

'''
{
    "interface_type": "",
    "messages_types": [],
    "config_broker": {
        "host": "",
        "user": "",
        "password": "",
        "exchanges": [],
    },
    "exceptional_scenario": [],
    "steps_to_adapt": [{
        "method": "",
        "route": "",
    }],
    "steps_for_behave_normal": [{
        "method": "",
        "route": "",
    }],
}
'''