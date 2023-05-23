import openai
from EdgeGPT import Chatbot, ConversationStyle
import re
import requests
from dotenv.main import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ['OPENAI_KEY']
NINJA_KEY = os.environ['NINJA_KEY']

def openai_response(prompt, personality = "You are a helpful assistant."):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content":
            personality},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        n=1,
        stop=["\nUser:"]
    )
    return response["choices"][0]["message"]["content"]

async def bing_response(prompt):
    bot = await Chatbot.create()
    response = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.creative)
    for message in response["item"]["messages"]:
        if message["author"] == "bot":
            bot_response = message["text"]
    response = re.sub('(\[\^\d+\^\])|^.*?Bing. ', '', bot_response)
    await bot.close()
    return response

def bucketlist_response():
    api_url = 'https://api.api-ninjas.com/v1/bucketlist'
    response = requests.get(api_url, headers={'X-Api-Key': NINJA_KEY})
    if response.status_code == requests.codes.ok:
        return response.json()["item"]
    else:
        print("Error:", response.status_code, response.text)

def facts_response():
    api_url = 'https://api.api-ninjas.com/v1/facts?limit=1'
    response = requests.get(api_url, headers={'X-Api-Key': NINJA_KEY})
    if response.status_code == requests.codes.ok:
        return response.json()[0]["fact"]
    else:
        print("Error:", response.status_code, response.text)

def joke_response():
    api_url = 'https://api.api-ninjas.com/v1/jokes?limit=1'
    response = requests.get(api_url, headers={'X-Api-Key': NINJA_KEY})
    if response.status_code == requests.codes.ok:
        return response.json()[0]["joke"]
    else:
        print("Error:", response.status_code, response.text)

def quote_response(category):
    api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(category)
    response = requests.get(api_url, headers={'X-Api-Key': NINJA_KEY})
    if response.status_code == requests.codes.ok:
        return response.json()[0]["quote"]
    else:
        print("Error:", response.status_code, response.text)
