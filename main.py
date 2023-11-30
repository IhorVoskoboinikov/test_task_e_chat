import os
import threading
import requests
import json

import bot
from queue_producer import QueueProducer


def send_last_message(last_message, body):
    print(f" [queue] Received from RabbitMQ: {body}")

    external_api_url = os.getenv('EXTERNAL_API_URL')
    if external_api_url:
        payload = {'last_message': last_message}
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(external_api_url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            print(f" [queue] Status: {response.status_code}")
            print(f" [queue] POST request sent to {external_api_url}")
        except requests.exceptions.RequestException as e:
            print(f" [queue] Error sending POST request: {e}")
    else:
        print(" [queue] EXTERNAL_API_URL is not defined in the environment variables.")


def print_last_message(last_message, body):
    print(f" [queue] Received from RabbitMQ: {body}. Last message from chat bot: {last_message}")


def callback(ch, method, properties, body) -> None:
    body = body.decode('utf-8')
    last_message = bot.last_message

    if body == "send":
        send_last_message(last_message=last_message, body=body)
    elif body == "print":
        print_last_message(last_message=last_message, body=body)
    else:
        print("Error! Unknown command!")


conn = QueueProducer()
conn.open_connection()
conn.basic_consume(callback)

if __name__ == "__main__":
    tr_1 = threading.Thread(target=bot.bot_run)
    tr_2 = threading.Thread(target=conn.channel.start_consuming)
    print(' [queue] Waiting for messages from RabbitMQ.')

    tr_1.start()
    tr_2.start()

    tr_1.join()
    tr_2.join()
