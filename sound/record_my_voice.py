#!/usr/bin/python

import sys
import numpy as np
import scipy.io.wavfile as S
import matplotlib.pyplot as plt
import sounddevice as sd
import time
import os
sys.path.append('../')
import plotting as P
from pdf import PDF
import mymath as MYM
import mio as myIO

print('Remember you can use makemusic.py to generate audio files with specific frequencies')

if len(sys.argv) == 1:
    print('Just going to plot audio file')
    duration = 0
    PLAYBACK = 0
    RUNFFT = 0
elif len(sys.argv) == 2:
    print('Just going to plot and record for a certain duration')
    duration = np.double(sys.argv[1])
    PLAYBACK = 0
    RUNFFT = 0
elif len(sys.argv) == 3:
    print('Going to record, plot and play it back')
    duration = np.double(sys.argv[1])
    PLAYBACK = int(sys.argv[2])
    RUNFFT = 0
elif len(sys.argv) == 4:
    print('Going to run FFT as well')
    duration = np.double(sys.argv[1])
    PLAYBACK = int(sys.argv[2])
    RUNFFT = int(sys.argv[3])

#%%%%record_my_voice(time)
#%%%time = length of record in seconds
#%%%PLAYBACK = 1 for play recording back to user, 0 for off
#%%%RUNFFT = 1 to run FFT and 0 to do nothing

##Setup plotting
pp = PDF(1,plt)

##Record audio
fs = 8192
if duration > 0:
    ##RECORD AUDIO
    print('Start Recording')
    audio_long = sd.rec(int(duration * fs), samplerate=fs, channels=1)[:,0]
    time.sleep(duration)
    print('Recording Finished')
    ##Clip the first 0.5 seconds
    time_long = np.linspace(0,duration,len(audio_long))
    audio = audio_long[time_long>0.5]
    time = np.linspace(0,duration-0.5,len(audio))
    outarray = np.vstack((time,audio))
    myIO.dlmwrite('Audio.txt',outarray)
    scaled = np.int16(audio/np.max(np.abs(audio)) * 32767)
    S.write('test.wav',fs,scaled)
else:
    ##OTHERWISE JUST READ IT IN
    data = np.loadtxt('Audio.txt')
    print(np.shape(data))
    time = data[0,:]
    audio = data[1,:]
    
###Plot stream
plt.plot(time,audio)
plt.xlabel('Time (sec)')
plt.ylabel('Amplitude')
pp.savefig()

###Play back audio
if PLAYBACK:
    if os.name == 'nt':
        ##Windows System
        from playsound import playsound
        playsound('test.wav')
    else:
        os.system('aplay test.wav')

##Run the FFT
if RUNFFT:
    #Note that Middle C on piano is 261 Hz. However, if you play
    #the middle C from youtube the audio comes in at around 1300 Hz.
    #Thus you need to make the iterations below well over 1000 or you
    #won't actually capture that audio file
    #One issue might be that the microphone might be too soft.
    #Ok so if you run the piano note through the phone software you get a peak at 1300 Hz
    #if you run the same audio file through this software you get a massive peak at 1300 Hz
    #as well. However, If you zoom way the hell into the plot you will see a tiny spike
    #at 261 Hz. So more than likely the fundamental note is there but there's this high
    #frequency 1300 hz signal that's drowning it out
    #What would be cool to do is to grab the magnitudes of the frequencies from the FFT
    #plot and then run it through makemusic.py and see if you can recreate the signal 
    MYM.fft(audio,time,2000,1,pp) ##Change the 1 to a 2 if you want it to plot on the fly

pp.close()
