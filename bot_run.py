import os

import telebot
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
print(' [chat_bot] Chat Bot is running...')
bot = telebot.TeleBot(TOKEN)

last_message = None


def get_last_message() -> str | None:
    return last_message


@bot.message_handler(commands=["start"])
def inline(message) -> None:
    bot.send_message(
        message.chat.id,
        " [chat_bot] Welcome to our telegram bot! \n\nYou can send messages to the chat bot!"
    )


@bot.message_handler(content_types=["text"])
def handle_text_messages(message) -> None:
    global last_message
    last_message = message.text
    print(f" [chat_bot] Chat bot received message from: ID - {message.chat.id}! Message: {last_message}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
