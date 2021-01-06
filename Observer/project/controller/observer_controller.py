from project.subscriber.observer_subscriber import ObserverSubscriber
from flask import jsonify, request
from project import app
from time import sleep


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/start", methods=["POST"])
def start():
    ObserverSubscriber(request.json).start()
    print("Start OK")
    return jsonify({"msg": "ok"})
