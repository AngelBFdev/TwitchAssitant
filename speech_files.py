import speech_recognition as sr
from deep_translator import GoogleTranslator

def record_microphone(filename, time_limit = "None"):
    with sr.Microphone() as source:
        recognizer = sr.Recognizer()
        source.pause_threshold = 1
        audio = recognizer.listen(source, phrase_time_limit=time_limit, timeout=None)
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())

def audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="es-MX")
    except:
        print('Skipping unknown error')
