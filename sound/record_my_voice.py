#!/usr/bin/python

import sys
import numpy as np
import scipy.io.wavfile as S
import plotting as P
from pdf import *
import matplotlib.pyplot as plt
import sounddevice as sd
import time
import mymath as MYM
import mio as myIO

if len(sys.argv) == 1:
    print('Need length of time to record')
    sys.exit()
elif len(sys.argv) == 2:
    duration = np.float(sys.argv[1])
    PLAYBACK = 0
    RUNFFT = 0
elif len(sys.argv) == 3:
    duration = np.float(sys.argv[1])
    PLAYBACK = int(sys.argv[2])
    RUNFFT = 0
elif len(sys.argv) == 4:
    duration = np.float(sys.argv[1])
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

###Plot stream
plt.plot(time,audio)
plt.xlabel('Time (sec)')
plt.ylabel('Amplitude')
pp.savefig()

###Play back audio
if PLAYBACK:
    scaled = np.int16(audio/np.max(np.abs(audio)) * 32767)
    S.write('test.wav',fs,scaled)
    os.system('aplay test.wav')

##Run the FFT
if RUNFFT:
    MYM.fft(audio,time,5000,1,pp) ##Change the 1 to a 2 if you want it to plot on the fly

pp.close()
