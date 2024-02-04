import speech_recognition as sr
import pyttsx3
import openai

openai.api_key = "API KEY"

engine = pyttsx3.init() # Inizializza il motore text-to-speech
recognizer = sr.Recognizer() # Inizializza l'oggetto Recognizer

messages = [ {"role": "system", "content": 
              "You are a intelligent assistant."} ]


def parla(testo_da_leggere):
    engine.setProperty('voice', 'it')
    engine.setProperty('voice','com.apple.speech.synthesis.voice.Alessandra')
    engine.setProperty('rate', 145) 
    engine.say(testo_da_leggere) # Leggi il testo
    engine.runAndWait()# Attendi il completamento della lettura
    
def acquisisci_audio():# Cattura l'audio dal microfono
    with sr.Microphone() as source:
        print("Parla qualcosa...")
        audio = recognizer.listen(source)

        try:
            # Utilizza Google Web Speech API per riconoscere il testo dall'audio
            text = recognizer.recognize_google(audio,  language="it-IT")
            print("Hai detto:", text)
            return text
        except sr.UnknownValueError:
            print("Non è stato possibile riconoscere il testo.")
        except sr.RequestError as e:
            print("Errore durante la richiesta a Google Speech Recognition:", str(e))
        
def rispondi(message):
    if message:
            messages.append(
                {"role": "user", "content": (message)},
            )
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages,max_tokens = 50
            )
            reply = chat.choices[0].message.content 
            print(reply)
            return reply       

while True:     
    domanda = acquisisci_audio()
    print(domanda)
    risposta = rispondi(domanda)
    parla(risposta)

