# Python program to translate
# speech to text and text to speech

##FIRST GRAB ALL THE IMPORTS
import speech_recognition as sr
import pyttsx3
import scipy.io.wavfile as S
import sounddevice as sd
import time
import matplotlib.pyplot as plt
import numpy as np

# Initialize the recognizer
r = sr.Recognizer()

##Record audio
fs = 8192
duration = 5.0
print('Start Recording')
audio_long = sd.rec(int(duration * fs), samplerate=fs, channels=1)[:,0]
time.sleep(duration)
print('Recording Finished')
##Clip the first 0.5 seconds
time_long = np.linspace(0,duration,len(audio_long))
audioclip = audio_long[time_long>0.5]
timeclip = np.linspace(0,duration-0.5,len(audioclip))
##Clip the last 0.5 seconds
audio = audioclip[timeclip < duration - 0.5]
t = np.linspace(0,duration-1.0,len(audio))
##Plot it
plt.plot(t,audio)

##Write data to a wavfile
scaled = np.int16(audio/np.max(np.abs(audio)) * 32767)
S.write('test.wav',fs,scaled)

##Pull audio from wav file
recordedaudio = sr.AudioFile('test.wav')
with recordedaudio as source:
    audio = r.record(source)

# Using google to recognize audio
MyText = r.recognize_google(audio)
MyText = MyText.lower()

print("Words: ",MyText)

##SHow the plto
plt.show()
