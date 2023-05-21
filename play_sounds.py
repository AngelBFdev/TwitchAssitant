from pygame import mixer
from tempfile import TemporaryFile
from gtts import gTTS

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