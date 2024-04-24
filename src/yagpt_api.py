from datetime import datetime

from aiohttp import ClientSession
from aiogram.types import Message
class YandexGpt:
    def __init__(self, api_key: str, dir_id: str):
        self.api_str = api_key
        self.url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
        self.dir_id = dir_id

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_str}",
        }

    def get_param(self):
        return {
            "modelUri": f"gpt://{self.dir_id}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": "1000"
            },
        }

async def ya_answer(yandex_gpt: YandexGpt, message: Message, addion_info: str) -> str:
    """
       Asynchronously posts a formatted query to Yandex API and returns a response.

       Args:
           yandex_gpt (YandexGpt): An object containing the Yandex GPT configuration.
           message (Message): The message object containing date and text.
           session (ClientSession): A session for making HTTP requests.

       Returns:
           str: The response message from Yandex GPT or an error message.
       """
    question = f"Сейчас: {message.date.strftime('%Y-%m-%d')} - {message.date.strftime('%H:%M:%S')} - {message.date.strftime('%A')}\n{message.text}\n[DATA]\n{addion_info}"
    try:
        async with ClientSession() as session:
            data = yandex_gpt.get_param()
            data['messages'] = [
                {
                    "role": "system",
                    "text": "Ты - помощник по учебе в ИТМО. Коротко и точно ответь на вопрос используя информацию в [DATA]. Используй всю релевантную из DATA информацию."
                },
                {
                    "role": "user",
                    "text": f"{question}"
                }
            ]
            response = await session.post(
                url=yandex_gpt.url,
                headers=yandex_gpt.get_headers(),
                json=data
            )
            response.raise_for_status()
            json_response = await response.json()
            return json_response['result']['alternatives'][0]['message']['text']
    except Exception as e:
        return "Failed to get answer"

async def ya_extract_date(yandex_gpt: YandexGpt, message: Message) -> str:
    try:
        today = message.date.strftime('%Y-%m-%d')
        system_msg = f"Найди дату в тексте\nОтвет выдай дату формате yyyy-mm-dd\nСегодня {today}"
        async with ClientSession() as session:
            data = yandex_gpt.get_param()
            data['messages'] = [
                {
                    "role": "system",
                    "text": system_msg
                },
                {
                    "role": "user",
                    "text": f"{message.text}"
                }
            ]
            data["completionOptions"]["maxTokens"] = "20"
            response = await session.post(
                url=yandex_gpt.url,
                headers=yandex_gpt.get_headers(),
                json=data
            )
            response.raise_for_status()
            json_response = await response.json()
            return json_response['result']['alternatives'][0]['message']['text']
    except Exception as e:
        return "Failed to get answer"






