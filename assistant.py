from play_sounds import play_music, play_text
from speech_files import record_microphone, audio_to_text
import apis
import time
from deep_translator import GoogleTranslator

class Assistant:
    def __init__(
            self, 
            intro_sound, 
            outro_sound, 
            lang = 'es', 
            input_file = 'input.wav',
            personality = 'You are a helpful assistant.'
        ):
        self.lang = lang
        self.input_file = input_file
        self.intro_sound = intro_sound
        self.outro_sound = outro_sound
        self.personality = personality
        self.speech_file()
        self.translator = GoogleTranslator(source='en', target='es')

    def confirmation_sound(self):
        play_music(self.intro_sound)

    def error_sound(self):
        play_music(self.outro_sound)

    def listen(self, time_limit = "None"):
        self.confirmation_sound()
        record_microphone(self.input_file, time_limit)
        phrase = audio_to_text(self.input_file)
        print(f"You said: {phrase}")
        
        return phrase
    
    def openai_response(self, time_limit = "None"):
        response = apis.openai_response(self.listen(time_limit), self.personality)
        self.speech_file(response)
        return response
    
    async def bing_response(self, time_limit = "None"):
        response = await apis.bing_response(self.listen(time_limit))
        self.speech_file(response)
        return response
    
    def bucketlist_response(self):
        response = apis.bucketlist_response()
        self.speech_file(response)
        es_response = self.translator.translate(response)
        return es_response
    
    def facts_response(self):
        response = apis.facts_response()
        self.speech_file(response)
        es_response = self.translator.translate(response)
        return es_response
    
    def speech_file(self, response = ""):
        with open('assistant_says.txt', "w", encoding='utf-8') as f:
            f.write(response)
        self.said_time = time.time()
        