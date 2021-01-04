from project import app
from flask import jsonify, request
from time import sleep


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/start", methods=["GET"])
def start():
    body = request.json
    return jsonify()
