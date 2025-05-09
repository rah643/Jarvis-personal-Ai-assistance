import queue
import json
import speech_recognition as sr
import webbrowser
import pyttsx3
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import requests


r=sr.Recognizer()

engine=pyttsx3.init()


#speak function
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Audio queue for incoming mic data
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(f"Status: {status}")
    q.put(bytes(indata))

def recognize_vosk():
    # Load the model
    model = Model("model")  # folder should be named 'model'
    samplerate = 16000
    recognizer = KaldiRecognizer(model, samplerate)

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🎤 Listening...")
        speak("I am listening.")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                return result.get("text", "")

def processCommand(c):
    if "oh my god" in c['text']:
        webbrowser.open("https://google.com")
    elif "you" in c['text']:
        webbrowser.open("https://youtube.com")
    elif "wow" in c['text']:
        webbrowser.open("https://web.whatsapp.com/")
    elif "" in c['text']:
        webbrowser.open("https://chatgpt.com/")
   

    

if __name__=="__main__":
    speak("Initailizing Jarvis....")

    while True:

        #obtain audion from microphone


        


        #recognise speech using google
        print("Recognizing......")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                print("Listening>>>>>>")
                audio=r.listen(source,timeout=5,phrase_time_limit=10)
            word=r.recognize_vosk(audio)
            s=json.loads(word)
            print(s)
            if(s['text']=="okay"):
                speak("ya")
                #listen for command
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    print("Jarvis Active")
                    audio=r.listen(source)
                    command=r.recognize_vosk(audio)
                    c=json.loads(command)
                    print(c)

                    processCommand(c)

                
        except sr.UnknownValueError:
            print("Jarvis cannot understand the audio")
        except sr.RequestError as e:
            print(f"listening error:{e}")
        

