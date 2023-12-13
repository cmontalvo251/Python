#!/usr/bin/python
import numpy as np
import os
import scipy.io.wavfile as S
import sounddevice as sd
import sys
sys.path.append('../')
import plotting as P
from pdf import PDF
import mymath as MYM
import mio as myIO


###THIS ROUTINE WILL TEST YOUR COMPUTER TO GENERATE AUDIO FILES

pi = np.pi

samplingFrequency = 8192;

notelength = 0.5;
tnote = np.linspace(0,notelength,samplingFrequency*notelength); #%%seconds
freq = 261.625; #%%Hz
amp = 1;
ynote1 = amp*np.cos(2*pi*freq*tnote);
ynote2 = amp*np.cos(2*pi*freq*tnote);
ynote3 = amp*np.cos(2*pi*freq*tnote);
ynote4 = amp*np.cos(2*pi*freq*tnote);

ynote_all = np.concatenate((ynote1,ynote2,ynote3,ynote4));

#Convert to integers - aplay doesn't support 64 bit wav files
scaled = np.int16(ynote_all/np.max(np.abs(ynote_all)) * 32767)
S.write('test.wav',samplingFrequency,scaled)
os.system('aplay test.wav')
time = np.linspace(0,notelength*4,len(scaled))
outarray = np.vstack((time,scaled))
myIO.dlmwrite('Audio.txt',outarray)


#% Copyright - Carlos Montalvo 2018
#% You may freely distribute this file but please keep my name in here
#% as the original owner

