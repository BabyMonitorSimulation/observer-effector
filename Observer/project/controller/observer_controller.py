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
    "interface_type": "broker",
    "config_broker": {
        "host": "localhost",
        "user": "guest",
        "password": "guest",
        "port": "15672",
        "exchanges": ["exchange_baby_monitor"]
    },
    "exceptional_scenario": [
        {"topic": "tv_msg", "type": "notificaiton"},
        {"topic": "tv_info", "msg": "blocked"}
    ],
    "normal_messages": [
        {"topic": "bm_info","type": "status"}
    ],
    "critical_messages":[
        {"topic": "bm_info", "type": "notification"}
    ],
    "steps_to_adapt": [{
        "method": "POST",
        "url": "http://localhost:5000/change_tv_status",
        "boby": {
            "lock": false
        }
    }],
    "steps_for_behave_normal": [{
        "method": "POST",
        "url": "http://localhost:5000/change_tv_status",
        "boby": {
            "lock": true
        }
    }]
}
'''