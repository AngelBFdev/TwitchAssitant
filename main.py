import keyboard
from play_sounds import play_text, play_audio
import asyncio
from assistant import Assistant

CHAT_PHRASE = "hey"
BING_PHRASE = "escúchame"
BUCKET_PHRASE = "deberíamos"
FACTS_PHRASE = "dime"
QUOTES_PHRASE = "cita"
JOKES_PHRASE = "chiste"

async def main():
    Navi = Assistant()

    while True:
        response = "Okay"
        try:
            if keyboard.read_key() == "+":
                phrase = Navi.listen(5)

                if 'personalidad' in phrase.lower():
                    if 'triste' in phrase.lower():
                        mood = 'sad'
                    elif 'alegre' in phrase.lower():
                        mood = 'happy'
                    elif 'tímida' in phrase.lower():
                        mood = 'shy'
                    elif 'agresiva' in phrase.lower():
                        mood = 'aggressive'

                    if 'dulces' in phrase.lower():
                        quirk = 'candy'
                    elif 'anime' in phrase.lower():
                        quirk = 'desu'
                    elif 'cristo' in phrase.lower():
                        quirk = 'crist'
                    elif 'rol' in phrase.lower():
                        quirk = 'rol'

                    Navi.personality([mood,quirk])

                elif BUCKET_PHRASE in phrase.lower():
                    Navi.bucketlist_response()

                elif QUOTES_PHRASE in phrase.lower():
                    category = phrase.split()[-1]
                    Navi.quote_response(category)

                elif JOKES_PHRASE in phrase.lower():
                    Navi.joke_response()

                elif FACTS_PHRASE in phrase.lower():
                    Navi.facts_response()

                elif BING_PHRASE in phrase.lower():
                    await Navi.bing_response(9)

                elif CHAT_PHRASE in phrase.lower():
                    Navi.openai_response(9)

            elif keyboard.read_key() == "}":
                Navi.openai_response(11)

            elif keyboard.read_key() == "{":
                Navi.delete_text()

        except Exception as e:
            Navi.error_sound()
            print("An error occurred: {}".format(e))

if __name__ == "__main__":
    asyncio.run(main())
