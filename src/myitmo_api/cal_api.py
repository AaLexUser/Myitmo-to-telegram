from datetime import date
import logging

from aiohttp import ClientSession
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)

_API_BASE_URL = "https://my.itmo.ru/api"


def _get_date_range_params() -> dict:
    """Produces start and end dates to request events of current academic term"""
    pivot = date.today().replace(month=8, day=1)
    this_year = date.today().year
    term_start_year = this_year - 1 if date.today() < pivot else this_year
    return dict(
        date_start=f"{term_start_year}-08-01",
        date_end=f"{term_start_year + 1}-07-31",
    )


async def _get_calendar_data(session: ClientSession, token: str, path: str) -> str:
    url = _API_BASE_URL + path
    params = _get_date_range_params()
    logger.info(f"Getting data from {url}, using params {params}")
    headers = {'Authorization': 'Bearer ' + token,
               'Accept': 'application/json, text/plain, */*',
               'Accept-Encoding': 'gzip, deflate, br, zstd',
               'Accept-Language': 'ru',
               'User-Agent': UserAgent().random
               }
    resp = await session.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return await resp.json()


async def get_raw_schedule(session: ClientSession, token: str) -> list:
    resp_json = await _get_calendar_data(session, token, "/schedule/schedule/personal")
    days = resp_json["data"]
    return list(days)
