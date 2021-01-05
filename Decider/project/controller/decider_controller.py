from project.entity.decider_entity import Decider
from flask import jsonify, request
from project import app


decider = None


@app.route("/index", methods=["GET"])
def index():
    return jsonify({"msg": "ok"})


@app.route("/adapt", methods=["GET"])
def adapt():
    global decider
    decider.adapt()

    return jsonify({"msg": "Adaptation ocurred"})


@app.route("/behave_normal", methods=["GET"])
def behave_normal():
    global decider
    decider.behave_normal()

    return jsonify({"msg": "Returned to previous behavior"})


@app.route("/configure", methods=["POST"])
def configure():
    global decider
    decider = Decider(
        request.json["steps_to_adapt"], request.json["steps_for_behave_normal"]
    )
    print("Start OK")
    return jsonify({"msg": "ok"})


"""
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
"""
# [{"topic": "tv_msg", "type": "notificaiton"}, {"topic": "tv_info", "msg": "blocked"}]
