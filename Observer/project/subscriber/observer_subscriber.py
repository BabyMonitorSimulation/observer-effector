import pika
import json
import threading
from pyrabbit.api import Client
from project.util.data import add_new
import requests


class ObserverSubscriber(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.queue = "observer"
        self.config_broker = config["config_broker"]
        self.exceptional_scenario = config["exceptional_scenario"]
        self.essential_scenarios = []
        self.scenario_running = ""
        self.normal_messages = config["normal_messages"]
        self.critical_messages = config["critical_messages"]
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config_broker["host"])
        )
        self.call_one = True
        self.channel = self.connection.channel()
        self.channel.queue_declare(self.queue)
        self.subscribe_in_all_queues()

    def get_bindings(self):
        client = Client(
            f'{self.config_broker["host"]}:{self.config_broker["port"]}',
            self.config_broker["user"],
            self.config_broker["password"],
        )

        bindings = client.get_bindings()
        bindings_result = [
            b for b in bindings if b["source"] in self.config_broker["exchanges"]
        ]

        return bindings_result

    def subscribe_in_all_queues(self):
        bindings = self.get_bindings()
        for bind in bindings:
            self.channel.queue_bind(
                exchange=bind["source"],
                queue=self.queue,
                routing_key=bind["routing_key"],
            )

        return bindings

    def callback(self, ch, method, properties, data):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        data = json.loads(data.decode("UTF-8"))
        current_scenario = data
        current_scenario["topic"] = method.routing_key
        print(f"Current Scenario: {current_scenario} - {self.scenario_running}")
        print(f"Exceptional Scenario: {self.exceptional_scenario}")
        is_essential_scenarios = False

        is_essential_scenarios = self.is_essential_scenarios(current_scenario)
        if is_essential_scenarios:
            self.essential_scenarios = add_new(
                self.essential_scenarios, current_scenario
            )

        except_scen = self.check_essential_exceptional()
        print(f"essential Scenario: {list(self.essential_scenarios)} \n\n")
        if except_scen and self.call_one:
            print("==== Cenário excepcional ====")
            requests.get(url=f"http://localhost:5002/adapt?scenario={self.scenario_running}")
            self.call_one = False

        # TODO: Como podemos pegar uma lista de cenários normais?
        # Por isso usamos self.normal_messages[0] por enquanto
        if self.check_normal_scenario(current_scenario) and except_scen:
            print("==== Cenário NORMAL ====")
            requests.get(
                url=f"http://localhost:5002/behave_normal?scenario={self.scenario_running}"
            )
            self.essential_scenarios = []
            self.call_one = True
            self.scenario_running = ''
            except_scen = False

    def run(self):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=False
        )

        self.channel.start_consuming()

    def stop(self):
        raise SystemExit()

    def check_normal_scenario(self, current_scenario):
        check = []
        for i in self.normal_messages:
            check=[]
            for k, v in current_scenario.items():
                if k in i.keys():
                    if v == i[k]:
                        check.append(True)
                    else:
                        check.append(False)
                if len(i) == check.count(True):
                    break
            if check.count(True) == len(i):
                return True
        return False

    def check_essential_exceptional(self):

        check = []
        if not self.essential_scenarios:
            return False

        for i in self.essential_scenarios:
            check.append(self.check_scenario(i))

        if check.count(True) == len(self.exceptional_scenario[self.scenario_running]):
            return True
        return False

    def check_scenario(self, current_scenario):
        is_excp = False
        for key, vl in self.exceptional_scenario.items():
            for i in self.exceptional_scenario[key]:
                check = []
                for k, v in current_scenario.items():
                    if k in i.keys():
                        if i[k] == v:
                            check.append(True)
                        else:
                            check.append(False)
                    if i["body"] != "*":
                        if k in i["body"].keys():
                            if i["body"][k] == v:
                                check.append(True)
                            else:
                                check.append(False)

                if i["body"] != "*":
                    if check.count(True) == len(i):
                        is_excp = True
                        break
                else:
                    if check.count(True) == len(i) - 1:
                        is_excp = True
                        break
            if is_excp:
                self.scenario_running = key
        return is_excp

    def is_essential_scenarios(self, current_scenario):
        if self.essential_scenarios == self.exceptional_scenario:
            return False

        return self.check_scenario(current_scenario)
