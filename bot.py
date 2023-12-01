import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)

dp = Dispatcher()

last_message = None


def get_last_message() -> str | None:
    return last_message


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer(" [chat_bot] Welcome to our telegram bot!\n\nYou can send messages to the chat bot!")


@dp.message(F.text)
async def handle_text_messages(message: types.Message) -> None:
    global last_message
    last_message = message.text
    print(f" [chat_bot] Chat bot received message from: ID - {message.chat.id}! Message: {last_message}")


async def bot_run() -> None:
    print(' [chat_bot] Chat Bot is running...')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(bot_run())
