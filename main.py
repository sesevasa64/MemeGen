import sys
import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv
load_dotenv()


def validate_proxy(proxy):
    return proxy if proxy != "" else None


TOKEN = getenv("BOT_TOKEN")
PROXY_RUL = validate_proxy(getenv("PROXY_URL"))

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main():
    session = AiohttpSession(proxy=PROXY_RUL)
    bot = Bot(TOKEN, session=session, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
