import asyncio

from dotenv import load_dotenv
from queue_producer import AsyncQueueProducer

load_dotenv()


async def main() -> None:
    conn = AsyncQueueProducer()
    await conn.open_connection()
    while True:
        message_from_user = input("Enter command 'send' or 'print' to RabbitMQ (or 'exit' to quit): ")
        if message_from_user.lower() == 'exit':
            break
        elif message_from_user.lower() not in ["print", 'send']:
            print("You can only add a 'print' or 'send' command to the queue!\nTry again!")
            continue

        await conn.add_to_queue(message_from_user)


if __name__ == "__main__":
    asyncio.run(main())
