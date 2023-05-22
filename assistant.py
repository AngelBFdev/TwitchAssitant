import speech_recognition as sr
from play_sounds import play_music, play_text
from speech_files import record_microphone, audio_to_text

class Assistant:
    def __init__(self, intro_sound, outro_sound, lang = 'es', input_file = 'input.wav'):
        self.lang = lang
        self.input_file = input_file
        self.intro_sound = intro_sound
        self.outro_sound = outro_sound

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
    