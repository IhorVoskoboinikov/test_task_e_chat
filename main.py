import threading

from bot_run import bot, get_last_message
from queue_producer import QueueProducer


def callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if body == "send":
        print(f" [queue] Received from RabbitMQ: {body}")
    elif body == "print":
        print(f" [queue] Received from RabbitMQ: {body}. Last message from chat bot: {get_last_message()}")
    else:
        print("error!")


conn = QueueProducer()
conn.open_connection()
conn.basic_consume(callback)

if __name__ == "__main__":
    tr_1 = threading.Thread(target=bot.polling, kwargs={"none_stop": True})
    tr_2 = threading.Thread(target=conn.channel.start_consuming)
    print(' [queue] Waiting for messages from RabbitMQ.')

    tr_1.start()
    tr_2.start()

    tr_1.join()
    tr_2.join()
