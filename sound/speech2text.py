# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

##Record audio
fs = 8192
print('Start Recording')
audio_long = sd.rec(int(duration * fs), samplerate=fs, channels=1)[:,0]
time.sleep(duration)
print('Recording Finished')
##Clip the first 0.5 seconds
time_long = np.linspace(0,duration,len(audio_long))
audio = audio_long[time_long>0.5]
time = np.linspace(0,duration-0.5,len(audio))

#listens for the user's input
audio = r.listen(sr.Microphone())
			
# Using google to recognize audio
MyText = r.recognize_google(audio)
MyText = MyText.lower()

print("Words: ",MyText)