import openai
import pyttsx3
import speech_recognition as sr
import time
from gtts import gTTS
from pygame import mixer
from tempfile import TemporaryFile
from dotenv.main import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ['OPENAI_KEY']

engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language='es-MX')
    except:
        print('Skipping unknown error')

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def speak_text(text):
    #engine.say(text)
    #engine.runAndWait()
    mixer.init()
    sf = TemporaryFile()
    
    tts = gTTS(text=text, lang='es')
    tts.write_to_fp(sf)
    sf.seek(0)
    mixer.music.load(sf) # escuchar el archivo creado
    mixer.music.play()

def main():
    while True:
        print("Say 'Genius' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            recognizer.energy_threshold = 200000
            audio = recognizer.listen(source)
            print(audio)
            try:
                transcription = recognizer.recognize_google(audio, language='es-MX')
                if 'navi' in transcription.lower():
                    mixer.init()
                    mixer.music.load("NaviSound.mp3") # escuchar el archivo creado
                    mixer.music.play()
                    mixer.get_busy()
                    filename = "input.wav"
                    print("Say your question...")
                    speak_text("Cual es tu pregunta?")                    
                    with sr.Microphone() as source:
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"You said: {text}")

                        #response = generate_response(text)
                        response = "Entiendo"
                        print(f"GPT-3 says: {response}")

                        speak_text(response)
                else:
                    print(transcription)

            except Exception as e:
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()