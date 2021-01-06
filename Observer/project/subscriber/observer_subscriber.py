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
        client = Client(f'{self.config_broker["host"]}:{self.config_broker["port"]}',
                        self.config_broker["user"],
                        self.config_broker["password"])

        bindings = client.get_bindings()
        bindings_result = [b for b in bindings if b["source"] in self.config_broker["exchanges"]]

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

        current_scenario = {"topic": method.routing_key, "type": data["type"]}
        print(f'Current Scenario: {current_scenario}')
        print(f'Exceptional Scenario: {self.exceptional_scenario}')
        is_essential_scenarios = self.is_essential_scenarios(current_scenario)
        if is_essential_scenarios:
            self.essential_scenarios = add_new(self.essential_scenarios,
                                               current_scenario)

        except_scen = self.essential_scenarios == self.exceptional_scenario
        print(f'essential Scenario: {list(self.essential_scenarios)} \n\n')
        if except_scen and self.call_one:
            print("==== Cenário excepcional ====")
            requests.get(url='http://localhost:5002/adapt')
            self.call_one = False

        # TODO: Como podemos pegar uma lista de cenários normais?
        # Por isso usamos self.normal_messages[0] por enquanto
        if current_scenario == self.normal_messages[0] and except_scen:
            print('==== Cenário NORMAL ====')
            requests.get(url='http://localhost:5002/behave_normal')
            self.essential_scenarios = []
            self.call_one = True

    def run(self):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=False
        )

        self.channel.start_consuming()

    def stop(self):
        raise SystemExit()

    def is_essential_scenarios(self, current_scenario):
        if self.essential_scenarios == self.exceptional_scenario:
            return False

        index_scenario = len(self.essential_scenarios)
        if current_scenario == self.exceptional_scenario[index_scenario]:
            return True

        return False
