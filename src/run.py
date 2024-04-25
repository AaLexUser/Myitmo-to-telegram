import asyncio

from aiogram import Dispatcher
from dotenv import load_dotenv

from handlers import router
from bot import get_bot

dp = Dispatcher()

load_dotenv()
async def main():
    dp.include_router(router)
    await dp.start_polling(get_bot())

if __name__ == '__main__':
    asyncio.run(main())
