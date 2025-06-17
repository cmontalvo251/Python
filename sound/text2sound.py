#!/usr/bin/python
import numpy as np
import sys
import scipy.io.wavfile as S
import os
import matplotlib.pyplot as plt
import sounddevice as sd

#%%%READ THIS 
#%%https://learn.adafruit.com/circuit-playground-o-phonor/musical-note-basics

#%%%Let's play the C major scale (CDEFGAB)
#%%%To get the frequencies we start with middle c
#%low_c = 65.406;
#%bass_c = 130.813;
middle_c = 261.6


#%%%moving up a note is equivalent to middle_c*2^(1/12)
#%%%thus 
#%middle_c*2^(1/12) = C sharp
#%middle_c*2^(2/12) = D
#%middle_c*2^(3/12) = D sharp
#%middle_c*2^(4/12) = E
#%For the key of C we have CDEFGAB thus
note_octaves = [0,2,4,5,7,9,11]
pi = np.pi

#%c_major_freq = middle_c*2.^(note_octaves/12)
#%[261.6 293.665 329.638 349.228 391.995 440 493.883]; %%%note frequency

#%%%We need to make a sine wave at these frequencies

if len(sys.argv) == 2:
    name = sys.argv[1]
    start_c = middle_c;
elif len(sys.argv) == 3:
    name = sys.argv[1]
    start_c = np.float(sys.argv[2])
else:
    print('Need Name and Start C')
    sys.exit()

#%%%Note the sample frequency is 8192 Hz /sec. Which means if we want a note
#%%%that lasts 1 second we need 8192 data points
FS = 8192
note_length = 0.2 #%%seconds

time = np.linspace(0,note_length,int(FS*note_length))

#%%%%Remember that natural frequency is 2*pi*f thus our sin wave is:
y = []
alphabet = 'abcdefghijklmnopqrstuvwxyz'

##Loop through name
for letter in name:
    #print letter
    ##Search for name in alphabet
    idx = alphabet.find(letter)
    #print idx
    if idx == -1:
         print('character not allowed: '+letter)
    else:
        octave = 0;
        #%%Remember that 8 is an extra octave thus we should hear middle c and
        # %%then an octave higher
        while idx > len(note_octaves): #%%If we overwrap we need to up the octave
            idx = idx - len(note_octaves);
            octave = octave + 1;
        freq = start_c*pow(2,(note_octaves[idx-1]/12.0+octave))
        print(letter+' '+str(freq))
        y = np.append(y,np.sin(2*pi*freq*time),axis=0)

y_np = np.asarray(y)        
#print np.shape(y_np)
scaled = np.int16(y_np/np.max(np.abs(y_np)) * 32767)
S.write('test.wav',FS,scaled)
if os.name == 'nt':
    ##Windows system
    from playsound import playsound
    playsound('test.wav')
else:
    os.system('aplay test.wav')

plt.plot(y_np)
plt.show()

# %%%So to make this work what we want to do is map every letter of the
# %%%alphabet to a note in the key of c. That is A = middle C, B = D, C = E
# %%%and so on. Might be pretty cool. Perhaps certain names sound cool and
# %%%others do not. It will also be a way to learn everyone's name.

# % Copyright - Carlos Montalvo 2018
# % You may freely distribute this file but please keep my name in here
# % as the original owner

