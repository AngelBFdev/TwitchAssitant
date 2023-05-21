import keyboard
from play_sounds import play_music, play_text
import speech_recognition as sr
import openai
from dotenv.main import load_dotenv
import os

load_dotenv()
openai.api_key = os.environ['OPENAI_KEY']

navi_personality = """
    Desde ahora eres Navi, una chica que le encanta estar dando 
    consejos, aun cuando nadie te los haya pedido. Estas obsesionada 
    con La Leyenda de Zelda y te gusta actuar como Navi, la hada molesta 
    del juego."""

filename = "input.wav"
navi_intro = "NaviIntro.mp3"
navi_outro = "NaviOutro.mp3"
chat_phrase = "hablemos"

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
        prompt=navi_personality + prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

def main():
    while True:
        if keyboard.read_key() == "}":
            play_music(navi_intro)
            try:
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=5, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())
                
                text = transcribe_audio_to_text(filename)
                print(f"You said: {text}")

                if 'hablemos' in text.lower():
                    play_music(navi_intro)
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=10, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    
                    text = transcribe_audio_to_text(filename)
                    print(f"You said: {text}")
                    response = generate_response(text)
                    play_text(response)
                else:
                    response = "Entiendo"
                    play_text(response)
                print(f"NAVI said: {response}")

            except Exception as e:
                play_music(navi_outro)
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()