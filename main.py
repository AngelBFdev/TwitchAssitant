import keyboard
from play_sounds import play_music, play_text
import openai
from dotenv.main import load_dotenv
import os
import asyncio
from EdgeGPT import Chatbot, ConversationStyle
import re
from assistant import Assistant

load_dotenv()
openai.api_key = os.environ['OPENAI_KEY']

NAVI_PERSONALITY = """
    Desde ahora eres Navi, una chica que le encanta estar dando 
    consejos, aun cuando nadie te los haya pedido. Estas obsesionada 
    con La Leyenda de Zelda y te gusta actuar como Navi, la hada molesta 
    del juego."""

INPUT_FILE = "input.wav"
INTRO_SOUND = "NaviIntro.mp3"
OUTRO_SOUND = "NaviOutro.mp3"
CHAT_PHRASE = "hablemos"
BING_PHRASE = "hey"
STARTING_LANGUAGE = "es"

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=NAVI_PERSONALITY + prompt,
        max_tokens=250,
        n=1,
        stop=None,
        temperature=0.6,
    )
    return response["choices"][0]["text"]

async def main():
    Navi = Assistant(INTRO_SOUND, OUTRO_SOUND, STARTING_LANGUAGE, INPUT_FILE)
    
    while True:
        response = "Okay"
        if keyboard.read_key() == "}":
            try:
                phrase = Navi.listen(5)

                if CHAT_PHRASE in phrase.lower():
                    response = generate_response(Navi.listen(10))

                elif 'portugués' in phrase.lower():
                    Navi.lang = "pt"

                elif 'español' in phrase.lower():
                    Navi.lang = "es"
                
                elif 'inglés' in phrase.lower():
                    Navi.lang = "en"
                    
                elif BING_PHRASE in phrase.lower():
                    bot = await Chatbot.create()
                    response = await bot.ask(prompt="", conversation_style=ConversationStyle.creative)
                    for message in response["item"]["messages"]:
                        if message["author"] == "bot":
                            bot_response = message["text"]
                    response = re.sub('(\[\^\d+\^\])|^.*?Bing. ', '', bot_response)
                    print("Bot's response:", bot_response)
                    await bot.close()

                play_text(response, Navi.lang)
                print(f"NAVI said: {response}")

            except Exception as e:
                Navi.error_sound()
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    asyncio.run(main())