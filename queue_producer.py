import os
import pika
from dotenv import load_dotenv

load_dotenv()


class QueueProducer:
    def __init__(self) -> None:
        self.amqp_user = os.getenv('AMQP_USER')
        self.amqp_password = os.getenv('AMQP_PASSWORD')
        self.amqp_address = os.getenv('AMQP_ADDRESS')
        self.amqp_vhost = os.getenv('AMQP_VHOST')
        self.amqp_port = int(os.getenv('AMQP_PORT'))
        self.queue_name = '0'
        self.channel = None

    def open_connection(self):
        credentials = pika.PlainCredentials(self.amqp_user, self.amqp_password)
        parameters = pika.ConnectionParameters(self.amqp_address, self.amqp_port, self.amqp_vhost, credentials)

        connection = pika.BlockingConnection(parameters)
        self.channel = connection.channel()

        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def add_to_queue(self, message: str) -> None:
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        print(f" [x] Sent '{message}'")

    def basic_consume(self, callback):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
