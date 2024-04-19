import asyncio
import datetime

from dotenv import load_dotenv
from aiogram import Dispatcher
from src.bot.handlers import router
from src.bot.bot import get_bot
import os

dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(get_bot())

if __name__ == '__main__':
    asyncio.run(main())
