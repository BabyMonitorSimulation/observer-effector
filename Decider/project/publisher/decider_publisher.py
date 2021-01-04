import pika
import json
import threading
from time import sleep
from pyrabbit.api import Client


class DeciderPublisher(threading.Thread):
    def __init__(self, config):
        threading.Thread.__init__(self)
        self.queue = "observer"
        self.config_broker = config["config_broker"]
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config_broker["host"])
        )
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

    def callback(self, ch, method, properties, body):
        ch.basic_ack(delivery_tag=method.delivery_tag)
        body = json.loads(body.decode("UTF-8"))
        print(f"Receive {body}")


    def run(self):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=False
        )

        self.channel.start_consuming()

    def stop(self):
        raise SystemExit()

