import asyncio
import json
import os
from typing import Any

import aio_pika
import aiohttp
from dotenv import load_dotenv
from queue_producer import AsyncQueueProducer

import bot

load_dotenv()


async def send_last_message(last_message: str, body: str) -> None:
    print(f" [queue] Received from RabbitMQ: {body}")

    external_api_url = os.getenv('EXTERNAL_API_URL')
    if external_api_url:
        payload = {'last_message': last_message}
        headers = {'Content-Type': 'application/json'}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(external_api_url, data=json.dumps(payload), headers=headers) as response:
                    response.raise_for_status()
                    print(f" [queue] Status: {response.status}")
                    print(f" [queue] POST request sent to {external_api_url}")
        except aiohttp.ClientError as e:
            print(f" [queue] Error sending POST request: {e}")
    else:
        print(" [queue] EXTERNAL_API_URL is not defined in the environment variables.")


async def print_last_message(last_message: str, body: str) -> None:
    print(f" [queue] Received from RabbitMQ: {body}. Last message from chat bot: {last_message}")


async def callback(ch: Any, method: Any, properties: Any, body: bytes) -> None:
    body = body.decode('utf-8')
    last_message = bot.last_message

    if body == "send":
        await send_last_message(last_message=last_message, body=body)
    elif body == "print":
        await print_last_message(last_message=last_message, body=body)
    else:
        print("Error! Unknown command!")


async def process_message(message: aio_pika.abc.AbstractIncomingMessage):
    async with message.process():
        data = message.body.decode('utf-8')
        last_message = bot.last_message
        print(f"Received message from RabbitMQ: {data}")
        if data == "send":
            await send_last_message(last_message=last_message, body=data)
        elif data == "print":
            await print_last_message(last_message=last_message, body=data)
        else:
            print("Error! Unknown command!")


async def queue_run() -> None:
    print(' [queue] Waiting for messages from RabbitMQ.')
    conn = AsyncQueueProducer()
    connection = await conn.open_connection()
    await conn.basic_consume(callback=process_message)
    try:
        await asyncio.Future()
    finally:
        if connection:
            await connection.close()


async def main():
    await asyncio.gather(bot.bot_run(), queue_run())


if __name__ == "__main__":
    asyncio.run(main())
