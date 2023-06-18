from play_sounds import play_music, play_text
from speech_files import record_microphone, audio_to_text, write_file
import apis
import time
from deep_translator import GoogleTranslator
import json

PERSONALITIES = json.load(open('personalities.json'))

CONVERSATION_LIMIT = 20
OBS_TEXT='assistant_says.txt'
INPUT_FILE='input.wav'
LANGUAGE = "es"
INTRO_SOUND = "NaviIntro.mp3"
OUTRO_SOUND = "NaviOutro.mp3"

class Assistant:
    def __init__(
            self,
            intro_sound = INTRO_SOUND,
            outro_sound = OUTRO_SOUND,
            arr = ['shy','rol']):
        self.intro_sound = intro_sound
        self.outro_sound = outro_sound
        self.personality(arr)
        write_file(OBS_TEXT)

    def confirmation_sound(self):
        play_music(self.intro_sound)

    def error_sound(self):
        play_music(self.outro_sound)

    def delete_text(self):
        write_file(OBS_TEXT)

    def personality(self, arr):
        personality = f"{PERSONALITIES['intro']} {PERSONALITIES['mood'][arr[0]]} {PERSONALITIES['quirk'][arr[1]]} {PERSONALITIES['reinforment']}"
        memory = list()
        memory.append(
            { 'role': 'system', 'content': personality }
            )
        self.write_json(memory)

    def write_json(self, memory):
        with open("memory.json", "w") as f:
            json.dump(memory, f)

    def read_json(self):
        with open("memory.json") as f:
            data = json.load(f)
        return data

    def translate_text(self, phrase, og_lang='en', dest_lang='es'):
        translator = GoogleTranslator(source=og_lang, target=dest_lang)
        return translator.translate(phrase)

    def listen(self, time_limit = "None"):
        self.confirmation_sound()
        record_microphone(INPUT_FILE, time_limit)
        phrase = audio_to_text(INPUT_FILE)
        print(f"You said: {phrase}")

        return phrase

    def speak(self, response, es_response=""):
        write_file(OBS_TEXT, response)
        print(f"NAVI said: {response}")
        play_text(response if es_response == "" else es_response,
                  LANGUAGE)

    def openai_response(self, time_limit = "None", main=True, chat=""):
        memory = self.read_json()
        message = self.listen(time_limit) if main else chat
        memory.append(
            { 'role': 'user', 'content': message }
            )

        response = apis.openai_response(memory, memory=True)
        memory.append(
            { 'role': 'assistant', 'content': response }
            )

        if len(memory) > CONVERSATION_LIMIT:
            memory = memory[1:]
        self.write_json(memory)
        self.speak(response)
        return response

    async def bing_response(self, time_limit = "None"):
        response = await apis.bing_response(self.listen(time_limit))
        self.speak(response)
        return response

    def bucketlist_response(self):
        response = apis.bucketlist_response()
        es_response = self.translate_text(response)
        self.speak(response,es_response)
        return es_response

    def facts_response(self):
        response = apis.facts_response()
        es_response = self.translate_text(response)
        self.speak(response,es_response)
        return es_response

    def joke_response(self):
        response = apis.joke_response()
        es_response = self.translate_text(response)
        self.speak(response,es_response)
        return es_response

    def quote_response(self, category):
        en_category = self.translate_text(category,'es','en')
        print(en_category)
        response = apis.quote_response(en_category)
        es_response = self.translate_text(response)
        self.speak(response,es_response)
        return es_response
