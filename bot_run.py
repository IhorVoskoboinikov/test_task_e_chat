import os

import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
print(TOKEN, '.....')
bot = telebot.TeleBot(TOKEN)

last_message = None


@bot.message_handler(commands=["start"])
def inline(message):
    bot.send_message(
        message.chat.id,
        "Welcome to our telegram bot! \n\nYou can send messages to the chat bot!"
    )


@bot.message_handler(content_types=["text"])
def handle_text_messages(message):
    global last_message
    last_message = message.text
    print(f"Chat bot received message from: ID - {message.chat.id}!\nMessage: {last_message}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
