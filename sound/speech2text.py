# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

#listens for the user's input
audio2 = r.listen(source2)
			
# Using google to recognize audio
MyText = r.recognize_google(audio2)
MyText = MyText.lower()

print("You said: ",MyText)
