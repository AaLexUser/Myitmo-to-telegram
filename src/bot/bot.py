import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from src.bot.handlers import router
import os

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
