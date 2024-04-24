from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)


def get_bot() -> Bot:
    return bot
