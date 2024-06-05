import requests
import json
import base64

CLIENT_SECRET = "c4b653d2-6019-4c1e-b8f4-d371a61aa9a7"
AUTHORIZE_DATA = "MmZmNTYxNDctYzBiMC00YzA3LThjMTQtZWU3NDllYjczZGIxOmM0YjY1M2QyLTYwMTktNGMxZS1iOGY0LWQzNzFhNjFhYTlhNw=="
URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"


def generate_text(query):
    bearer = str(base64.b64encode(bytes(CLIENT_SECRET + AUTHORIZE_DATA)))

    payload = json.dumps({
    "model": "GigaChat",
    "messages": [
        {
        "role": "user",
        "content": query
        }
    ],
    "temperature": 1,
    "top_p": 0.1,
    "n": 1,
    "stream": False,
    "max_tokens": 512,
    "repetition_penalty": 1
    })

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer %s' % bearer
}

    response = requests.request("POST", URL, headers=headers, data=payload)
    return response.text


print(generate_text("Как дела?"))