import os
import pika

# Загрузка переменных окружения из файла .env
from dotenv import load_dotenv
load_dotenv()

# Получение настроек для подключения к RabbitMQ
AMQP_USER = os.getenv('AMQP_USER')
AMQP_PASSWORD = os.getenv('AMQP_PASSWORD')
AMQP_ADDRESS = os.getenv('AMQP_ADDRESS')
AMQP_VHOST = os.getenv('AMQP_VHOST')
AMQP_PORT = int(os.getenv('AMQP_PORT'))

# Создание параметров подключения
credentials = pika.PlainCredentials(AMQP_USER, AMQP_PASSWORD)
parameters = pika.ConnectionParameters(AMQP_ADDRESS, AMQP_PORT, AMQP_VHOST, credentials)
# connection = pika.BlockingConnection(parameters)
# channel = connection.channel()
# channel.queue_declare(queue='0', durable=True)
# Попытка установить соединение с RabbitMQ
try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Ваш код для работы с каналом и обменом сообщениями

except pika.exceptions.AMQPConnectionError as e:
    print(f"Ошибка подключения к RabbitMQ: {e}")


