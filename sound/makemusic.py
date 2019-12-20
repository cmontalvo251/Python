#!/usr/bin/python
import numpy as np
import os
import scipy.io.wavfile as S
import sounddevice as sd

###THIS ROUTINE WILL TEST YOUR COMPUTER TO GENERATE AUDIO FILES

pi = np.pi

samplingFrequency = 8192;

notelength = 0.08;
tnote = np.linspace(0,notelength,samplingFrequency*notelength); #%%seconds
freq = 200; #%%Hz
amp = 1;
ynote1 = amp*np.cos(2*pi*freq*tnote);
ynote2 = amp*np.cos(2*pi*300*tnote);
ynote3 = amp*np.cos(2*pi*350*tnote);
ynote4 = amp*np.cos(2*pi*400*tnote);

ynote_all = np.concatenate((ynote1,ynote2,ynote3,ynote4));

#Convert to integers - aplay doesn't support 64 bit wav files
scaled = np.int16(ynote_all/np.max(np.abs(ynote_all)) * 32767)
S.write('test.wav',samplingFrequency,scaled)
os.system('aplay test.wav')

#% Copyright - Carlos Montalvo 2018
#% You may freely distribute this file but please keep my name in here
#% as the original owner

