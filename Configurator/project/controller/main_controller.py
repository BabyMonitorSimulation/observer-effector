from project import app
from flask import jsonify, request
from time import sleep
import requests


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/start", methods=["GET"])
def start():
    body = request.json
    return jsonify({"msg": "ok"})


'''
{
    "interface_type": "",
    "messages_types": [],
    "exceptional_scenario": [],
    "steps_to_adapt": {
        "method": "",
        "route": "",
    },
    "steps_for_behave_normal": {
        "method": "",
        "route": "",
    },
}
'''
