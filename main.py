import keyboard
from play_sounds import play_text
import asyncio
from assistant import Assistant
import time
import os

NAVI_PERSONALITY = """De ahora en adelante eres Navi una chica 
    muy distraida que siempre está feliz. Te encantan los dulces 
    y siempre encuentras una manera de agregarlos a la conversación. 
    No ocupas presentarte, ya te conozco. 
    Recuerda, TU NO ERES UN PROGRAMA! Tu eres una chica real."""
INPUT_FILE = "input.wav"
INTRO_SOUND = "NaviIntro.mp3"
OUTRO_SOUND = "NaviOutro.mp3"
STARTING_LANGUAGE = "es"

CHAT_PHRASE = "hey"
BING_PHRASE = "escúchame"
BUCKET_PHRASE = "deberíamos"
FACTS_PHRASE = "dime"

async def main():
    Navi = Assistant(
        INTRO_SOUND, 
        OUTRO_SOUND, 
        STARTING_LANGUAGE, 
        INPUT_FILE,
        NAVI_PERSONALITY
        )
    
    while True:
        response = "Okay"
        try:
            if keyboard.read_key() == "}":
                phrase = Navi.listen(5)

                if 'portugués' in phrase.lower():
                    Navi.lang = "pt"

                elif 'español' in phrase.lower():
                    Navi.lang = "es"
                
                elif 'inglés' in phrase.lower():
                    Navi.lang = "en"
                
                elif BUCKET_PHRASE in phrase.lower():
                    response = Navi.bucketlist_response()

                elif FACTS_PHRASE in phrase.lower():
                    response = Navi.facts_response()

                elif BING_PHRASE in phrase.lower():
                    response = await Navi.bing_response(10)
                
                elif CHAT_PHRASE in phrase.lower():
                    response = Navi.openai_response(10)

                print(f"NAVI said: {response}")
                play_text(response, Navi.lang)

            elif (os.stat('assistant_says.txt').st_size != 0 and 
                time.time() - Navi.said_time > 30):
                Navi.speech_file()

        except Exception as e:
            Navi.error_sound()
            print("An error occurred: {}".format(e))

if __name__ == "__main__":
    asyncio.run(main())