import datetime
import json

from src.myitmo_api.auth import get_access_token
from dotenv import load_dotenv
from aiohttp import ClientSession
import os
from src.myitmo_api.cal_api import get_raw_schedule

SCHEDULE_FILE_PATH = 'schedule.json'
DATE_FORMAT = "%Y-%m-%d"
LESSON_SEPARATOR = "-" * 60


def load_config():
    load_dotenv()
    username = os.getenv("ISU_USERNAME")
    password = os.getenv("ISU_PASSWORD")
    if username is None or password is None:
        raise Exception("Missing ISU credentials")
    return username, password


async def update_schedule():
    try:
        username, password = load_config()
        async with ClientSession() as session:
            token = await get_access_token(session, username, password)
            schedule = await get_raw_schedule(session, token)
            with open(SCHEDULE_FILE_PATH, 'w') as outfile:
                json.dump(schedule, outfile)
    except Exception as e:
        print(f"Failed to update schedule: {e}")
        return False
    return True


def get_today_lessons(today_date: datetime.date):
    with open(SCHEDULE_FILE_PATH, 'r') as schedule_file:
        schedule_json = json.load(schedule_file)
    for item in schedule_json:
        item_date = datetime.datetime.strptime(item["date"], "%Y-%m-%d").date()
        if today_date.day == item_date.day and today_date.month == item_date.month and today_date.year == item_date.year:
            return format_lessons(item)
    return "No lessons today"

def get_lessons(date: datetime.date):
    with open(SCHEDULE_FILE_PATH, 'r') as schedule_file:
        schedule_json = json.load(schedule_file)
    for item in schedule_json:
        item_date = datetime.datetime.strptime(item["date"], "%Y-%m-%d").date()
        if date.day == item_date.day and date.month == item_date.month and date.year == item_date.year:
            lessons = format_lessons_json(item)
            if lessons is not None:
                return f"Пары на {date.strftime('%Y-%m-%d')}\n" + lessons
            break
    return f"No lessons for {date.strftime('%Y-%m-%d')}"



def format_lessons(item):
    if not item['lessons']:
        return "Сегодня пар нет"
    lessons_detail = []
    for lesson in item['lessons']:
        lesson_info = [
            LESSON_SEPARATOR,
            f"{lesson['time_start']}-{lesson['time_end']}\t{lesson['subject']}"
        ]
        if lesson['building']:
            lesson_info.append(f"\t\tbuilding: {lesson['building']}")
        if lesson['room']:
            lesson_info.append(f"\t\troom: {lesson['room']}")
        lesson_info.append(LESSON_SEPARATOR)
        lessons_detail.append('\n'.join(lesson_info))
    return '\n'.join(lessons_detail)

def format_lessons_json(item):
    if not item['lessons']:
        return None
    lessons_detail = []
    for lesson in item['lessons']:
        lesson_info = [
            f"{lesson['subject']}" + "{"
        ]
        if lesson['time_start']:
            lesson_info.append(f"start: {lesson['time_start']}")
        if lesson['time_end']:
            lesson_info.append(f"end: {lesson['time_end']}")
        if lesson['type']:
            lesson_info.append(f"type: {lesson['type']}")
        if lesson['building']:
            lesson_info.append(f"building: {lesson['building']}")
        if lesson['room']:
            lesson_info.append(f"room: {lesson['room']}")
        if lesson['teacher_name']:
            lesson_info.append(f"teacher: {lesson['teacher_name']}")
        if lesson['zoom_url']:
            lesson_info.append(f"zoom: {lesson['zoom_url']}")
        lesson_info.append("}")
        lessons_detail.append('\n'.join(lesson_info))
    return '\n'.join(lessons_detail)

