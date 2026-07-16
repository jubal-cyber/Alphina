import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 170)  # Speed
engine.setProperty("volume", 1.0)  # Volume (0.0 to 1.0)

engine.say("Hello! I am Rudy. Nice to meet you.")
engine.runAndWait()