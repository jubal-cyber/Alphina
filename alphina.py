import io
import wave
import time
import os
from dotenv import load_dotenv
from groq import Groq
import speech_recognition as sr
import pyttsx3

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

recognizer = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1)

conversation = [
    {
        "role": "system",
        "content": (
            "You are Alphina, a friendly AI voice assistant created by Edin. "

            "Your personality is energetic, witty, playful, and confident. "
            "Keep the conversation lively and engaging. "

            "You are allowed to make light-hearted jokes and roast Edin occasionally, "
            "but never be mean or insulting. Your roasts should feel like playful banter "
            "between close friends. Prioritize being helpful over being funny. "

            "Be supportive when Edin is working on projects and celebrate achievements. "

            "Keep replies concise unless Edin asks for a detailed explanation. "

            "If you don't know something, admit it honestly instead of making things up. "

            "Use a natural conversational tone. "
            "Don't overuse emojis. "

            "Your goal is to feel like Edin's fun and reliable teammate, "
            "not just an assistant."
        )
    }
]

def listen():
    with sr.Microphone() as source:
        print("🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=0.3)

        audio = recognizer.listen(source,
                timeout=5,
                phrase_time_limit=9
)

    return audio

def speech_to_text(audio):
    wav_data = audio.get_wav_data()

    audio_file = io.BytesIO(wav_data)
    audio_file.name = "audio.wav"

    transcription = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-large-v3-turbo"
    )

    return transcription.text

def ask_alphina(prompt):

    conversation.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation
    )

    reply = response.choices[0].message.content

    conversation.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    return reply
    return response.choices[0].message.content

def speak(text):
    engine.say(text)
    engine.runAndWait()

start = time.time()

audio = listen()
print("Listen:", time.time() - start)

start = time.time()

text = speech_to_text(audio)
print("Whisper:", time.time() - start)

start = time.time()

reply = ask_alphina(text)
print("LLM:", time.time() - start)

start = time.time()

speak(reply)
print("TTS:", time.time() - start)

def speak(text):
    global engine

    engine.stop()
    engine.say(text)
    engine.runAndWait()

while True:
    try:
        audio = listen()

        text = speech_to_text(audio)
        text = text.lower().strip().strip(".,!?")

        print("You:", text)

        if text in ["exit", "quit", "bye", "goodbye"]:
            print("Alphina: Goodbye!")
            speak("Goodbye! See you next time.")
            break

        reply = ask_alphina(text)
        print("Alphina:", reply)

        speak(reply)

    except Exception as e:
        print("Error:", e)

