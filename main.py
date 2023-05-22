import keyboard
from play_sounds import play_music, play_text
import speech_recognition as sr
import openai
from dotenv.main import load_dotenv
import os
import asyncio
from EdgeGPT import Chatbot, ConversationStyle
import re

load_dotenv()
openai.api_key = os.environ['OPENAI_KEY']

NAVI_PERSONALITY = """
    Desde ahora eres Navi, una chica que le encanta estar dando 
    consejos, aun cuando nadie te los haya pedido. Estas obsesionada 
    con La Leyenda de Zelda y te gusta actuar como Navi, la hada molesta 
    del juego."""

FILENAME = "input.wav"
NAVI_INTRO = "NaviIntro.mp3"
NAVI_OUTRO = "NaviOutro.mp3"
CHAT_PHRASE = "hablemos"
BING_PHRASE = "hey"

def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="es-MX")
    except:
        print('Skipping unknown error')

def record_microphone(time_limit = "None"):
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        source.pause_threshold = 1
        audio = recognizer.listen(source, phrase_time_limit=time_limit, timeout=None)
        with open(FILENAME, "wb") as f:
            f.write(audio.get_wav_data())

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

def confirmation_sound():
    play_music(NAVI_INTRO)

async def main():
    lang = "es"
    
    while True:
        response = "Okay"
        if keyboard.read_key() == "}":
            confirmation_sound()
            try:
                record_microphone(5)
                phrase = audio_to_text(FILENAME)
                print(f"You said: {phrase}")

                if CHAT_PHRASE in phrase.lower():
                    confirmation_sound()
                    record_microphone(10)
                    phrase = audio_to_text(FILENAME)
                    print(f"You said: {phrase}")
                    response = generate_response(phrase)

                elif 'portugués' in phrase.lower():
                    lang = "pt"

                elif 'español' in phrase.lower():
                    lang = "es"
                
                elif 'inglés' in phrase.lower():
                    lang = "en"
                    
                elif BING_PHRASE in phrase.lower():
                    bot = await Chatbot.create()
                    response = await bot.ask(prompt="", conversation_style=ConversationStyle.creative)
                    for message in response["item"]["messages"]:
                        if message["author"] == "bot":
                            bot_response = message["text"]
                    response = re.sub('(\[\^\d+\^\])|^.*?Bing. ', '', bot_response)
                    print("Bot's response:", bot_response)
                    await bot.close()


                play_text(response, lang)
                print(f"NAVI said: {response}")

            except Exception as e:
                play_music(NAVI_OUTRO)
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    asyncio.run(main())