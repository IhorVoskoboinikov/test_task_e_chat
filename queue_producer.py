import os
from typing import Callable

import aio_pika
from dotenv import load_dotenv

load_dotenv()


class AsyncQueueProducer:
    def __init__(self) -> None:
        self.amqp_user = os.getenv('AMQP_USER')
        self.amqp_password = os.getenv('AMQP_PASSWORD')
        self.amqp_address = os.getenv('AMQP_ADDRESS')
        self.amqp_vhost = os.getenv('AMQP_VHOST')
        self.amqp_port = int(os.getenv('AMQP_PORT'))
        self.queue_name = '0'
        self.channel = None

    async def open_connection(self) -> None:
        connection = await aio_pika.connect_robust(
            f"amqp://{self.amqp_user}:{self.amqp_password}@{self.amqp_address}:{self.amqp_port}/{self.amqp_vhost}",
        )
        self.channel = await connection.channel()
        await self.channel.set_qos(prefetch_count=100)

        await self.channel.declare_queue(self.queue_name, durable=True)

    async def add_to_queue(self, message: str) -> None:
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=self.queue_name
        )
        print(f" [x] Sent '{message}'")

    async def basic_consume(self, callback: Callable) -> None:
        queue = await self.channel.declare_queue(self.queue_name, durable=True)
        await queue.consume(callback)
