import requests
import uuid

import json
import warnings

warnings.simplefilter("ignore")




class GigaChatApi:
    CLIEND_ID = "2ff56147-c0b0-4c07-8c14-ee749eb73db1"
    CLIENT_SECRET = "22f47e3f-aa18-4f14-9c73-47692234db31"
    AUTH_DATA = "MmZmNTYxNDctYzBiMC00YzA3LThjMTQtZWU3NDllYjczZGIxOjIyZjQ3ZTNmLWFhMTgtNGYxNC05YzczLTQ3NjkyMjM0ZGIzMQ=="

    GET_TOKEN_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    GET_ANSWER_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    SYSTEM_PROMT = "Ты - голосовой асистент в моём приложении, тебя зовут Лолли, сейчас с тобой будет общаться пользователь"

    messages_history = []

    def __init__(self) -> None:
        self.messages_history += [
            {
                "role" : "system",
                "content" : self.SYSTEM_PROMT
            }
        ]

    def update_message_history(self,user_message,chat_answer):
        self.messages_history += [
            {
                "role" : "user",
                "content" : user_message
            },
            {
                "role" : "assistant",
                "content" : chat_answer
            }
        ]


    def get_answer(self, message):
        new_message = {
            "role" : "user",
            "content" : message
        }
        messages = self.messages_history + [new_message]
        payload = json.dumps({
            "model" : "GigaChat:latest",
            "messages" : messages
        })
        headers = {
            "Content-Type" : "application/x-www-form-urlencoded",
            "Accept" : "application/json",
            "RqUID" : str(uuid.uuid4()),
            "Authorization" : f"Bearer {self.token}"
        }
        response = requests.post(self.GET_ANSWER_URL,headers=headers,data=payload,verify=False)

        chat_message = response.json()["choices"][0]["message"]["content"]
        self.update_message_history(message,chat_message)
        return chat_message


    @property
    def token(self):
        payload = {
            "scope" : "GIGACHAT_API_PERS"
        }
        headers = {
            "Content-Type" : "application/x-www-form-urlencoded",
            "Accept" : "application/json",
            "RqUID" : str(uuid.uuid4()),
            "Authorization" : f"Basic {self.AUTH_DATA}"
        }
        response = requests.post(self.GET_TOKEN_URL,headers=headers,data=payload,verify=False)
        return response.json()["access_token"]



giga = GigaChatApi()