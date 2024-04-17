import json

from auth import get_access_token
from dotenv import load_dotenv
from aiohttp import ClientSession
import os
from cal_api import get_raw_schedule

username = os.getenv("ISU_USERNAME")
password = os.getenv("ISU_PASSWORD")


async def update_schedule():
    async with ClientSession() as session:
        token = await get_access_token(session, username, password)
        resp_json = await get_raw_schedule(session, token)
        with open('schedule.json', 'w') as outfile:
            json.dump(resp_json, outfile)



