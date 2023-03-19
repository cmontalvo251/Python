# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

#listens for the user's input
audio = r.listen(sr.Microphone())
			
# Using google to recognize audio
MyText = r.recognize_google(audio)
MyText = MyText.lower()

print("Words: ",MyText)