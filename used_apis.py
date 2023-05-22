import openai
from EdgeGPT import Chatbot, ConversationStyle
import re

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