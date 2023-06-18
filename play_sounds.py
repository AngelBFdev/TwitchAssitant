from pygame import mixer
from tempfile import TemporaryFile
from gtts import gTTS
from elevenlabs import generate, stream, set_api_key, play,voices
import os
from dotenv.main import load_dotenv
import pyttsx3

load_dotenv()
set_api_key(os.environ['ELEVEN_LABS_KEY'])

def play_music(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()

def play_text(text, lang):
    sf = TemporaryFile()
    tts = gTTS(text=text, lang=lang)
    tts.write_to_fp(sf)
    sf.seek(0)
    play_music(sf)

def pytts_play(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def play_audio(prompt):
    voices()
    audio = generate(
        text=prompt,
        voice="Myriam - Teen Girl",
        model="eleven_multilingual_v1"
        )
    play(audio)
