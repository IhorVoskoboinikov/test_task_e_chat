## Python applications with RabbitMQ and Docker for reading and processing messages from a telegram bot

Kitchen Service (CRUD application) is a web application for managing recipes, 
cooks, and dish types in a restaurant kitchen.


## Setup:

1. Clone the project:
+ ```git clone https://github.com/IhorVoskoboinikov/test_task_e_chat.git```
2. Create .env file with your data (look for example -> .env.example)
3. Up docker containers
+ ```docker-compose up```


## Usage local:

> 1. Go to the chat_bot in telegram and send to bot any text message, after which you will see this message in the console
> 2. You can add the commands in queue manually by running the file producer.py 
(for this you will need to install python and run command: ```python producer.py``` )
> 3. When you send command in queue you can see result in console
> 4. For test POST requests you can run local server test_api.py
(for this you will need to install python and run command: ```python test_api.py``` )
