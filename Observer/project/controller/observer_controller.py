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
# [{"topic": "tv_msg", "type": "notificaiton"}, {"topic": "tv_info", "msg": "blocked"}]
