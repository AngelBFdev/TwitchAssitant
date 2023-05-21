import keyboard
from play_sounds import play_music, play_text
import speech_recognition as sr
import openai
from dotenv.main import load_dotenv
import os

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

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language="es-MX")
    except:
        print('Skipping unknown error')

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

def main():
    lang = "es"
    response = "Entiendo"

    while True:
        if keyboard.read_key() == "}":
            confirmation_sound()
            try:
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=5, timeout=None)
                    with open(FILENAME, "wb") as f:
                        f.write(audio.get_wav_data())                
                text = transcribe_audio_to_text(FILENAME)
                print(f"You said: {text}")

                if CHAT_PHRASE in text.lower():
                    confirmation_sound()
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=10, timeout=None)
                        with open(FILENAME, "wb") as f:
                            f.write(audio.get_wav_data())
                    text = transcribe_audio_to_text(FILENAME)
                    print(f"You said: {text}")
                    response = generate_response(text)

                elif 'portugués' in text.lower():
                    lang = "pt"
                    confirmation_sound()

                elif 'español' in text.lower():
                    lang = "es"
                    confirmation_sound()
                
                elif 'inglés' in text.lower():
                    lang = "en"
                    confirmation_sound()

                play_text(response, lang)
                print(f"NAVI said: {response}")

            except Exception as e:
                play_music(NAVI_OUTRO)
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()