import asyncio
from datetime import date

import os
from time import strptime

import aiocron
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from bot import get_bot

from myitmo_api.app import *
from yagpt.yagpt_api import *


class GetLessonsArgs(StatesGroup):
    date_req = State()

# Constants
UNAUTHORIZED_MESSAGE = "Мама говорила с незнакомцами не разговаривать."

# Initialize Router
router = Router()

# Load environment variables
load_dotenv()
MY_TG_ID = os.getenv("MY_TG_ID")
if MY_TG_ID is None:
    raise ValueError("MY_TG_ID environment variable is not set")
YA_API_KEY = os.getenv("YA_API_KEY")
if YA_API_KEY is None:
    raise ValueError("YA_API_KEY environment variable is not set")
YA_DIR_ID = os.getenv("YA_DIR_ID")
if YA_DIR_ID is None:
    raise ValueError("YA_DIR_ID environment variable is not set")
yagpt = YandexGpt(YA_API_KEY, YA_DIR_ID)

class_reminder = None


async def send_daily_reminder(chat_id: int):
    today = date.today()
    lessons = get_lessons(today)
    await get_bot().send_message(chat_id=chat_id, text=lessons)


@router.message(Command('start_class_reminder'))
async def start_daily_review(message: Message):
    if message.from_user and str(message.from_user.id) == MY_TG_ID:
        global class_reminder
        if class_reminder is None:
            # specifies the schedule: at minute 0 of hour 9, every day of the month, every month, and every day of the week.
            class_reminder = aiocron.crontab('0 9 * * *', func=send_daily_reminder, args=(message.chat.id,))
            await message.reply("Daily class reminder enabled.")
        else:
            await message.reply("Daily class reminder was already enabled.")
    else:
        await message.reply(UNAUTHORIZED_MESSAGE)

@router.message(Command('stop_class_reminder'))
async def stop_auto(message: Message):
    if message.from_user and str(message.from_user.id) == MY_TG_ID:
        global class_reminder
        if class_reminder is None:
            await message.reply("Daily class reminder is not running.")
        else:
            await asyncio.sleep(10)
            if class_reminder: class_reminder.stop()
            await message.reply("Daily class reminder is disabled")
    else:
        await message.reply(UNAUTHORIZED_MESSAGE)

@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user and str(message.from_user.id) == MY_TG_ID:
        await message.answer(f'Привет, {message.from_user.first_name}!')
    else:
        await message.reply(UNAUTHORIZED_MESSAGE)

@router.message(Command('updateDB'))
async def cmd_update(message: Message):
    if message.from_user and str(message.from_user.id) == MY_TG_ID:
        res = await update_schedule()
        formatted_date = message.date.strftime("%Y-%m-%d %H:%M:%S")
        if res is True:
            await message.answer(f'База обновлена, {formatted_date}!')
        else:
            await message.answer(f'Failed to update schedule: {formatted_date}')
    else:
        await message.reply(UNAUTHORIZED_MESSAGE)


@router.message(Command('getTodayLessons'))
async def cmd_getTodayLessons(message: Message):
    if message.from_user and str(message.from_user.id) == MY_TG_ID:
        answer = get_today_lessons(message.date)
        await message.answer(answer)
    else:
        await message.reply(UNAUTHORIZED_MESSAGE)


@router.message(Command('getLessons'))
async def cmd_getLessons(message: Message, state: FSMContext):
    if message.from_user and str(message.from_user.id) == MY_TG_ID:
        await state.set_state(GetLessonsArgs.date_req)
        await message.answer("Please enter the date for which you want to see lessons (YYYY-MM-DD format):")
    else:
        await message.reply(UNAUTHORIZED_MESSAGE)


@router.message(GetLessonsArgs.date_req)
async def cmd_getLessonsArgs(message: Message, state: FSMContext):
    if message.from_user and str(message.from_user.id) == MY_TG_ID:
        try:
            date = strptime(message.text, "%Y-%m-%d").date()
        except ValueError:
            await message.answer("Invalid date format. Please enter in YYYY-MM-DD format.")
            return
        lessons = get_lessons(date)
        if not lessons:
            await message.answer("No lessons found for the provided date.")
            return
        await message.answer(lessons)
        await state.clear()
    else:
        await message.reply(UNAUTHORIZED_MESSAGE)

@router.message()
async def cmd_ya_answer(message: Message):
    if message.from_user and str(message.from_user.id) == MY_TG_ID:
        date_str = await ya_extract_date(yagpt, message)
        try:
            date = strptime(date_str, "%Y-%m-%d").date()
            lessons = get_lessons(date)
            if not lessons:
                await message.answer(f"No lessons found for the provided date: {date_str}")
            else:
                answer = await ya_answer(yagpt, message, lessons)
                await message.answer(answer)
        except Exception as e:
            await message.answer(f"The date was not correctly recognized. Try again")
    else:
        await message.reply(UNAUTHORIZED_MESSAGE)




