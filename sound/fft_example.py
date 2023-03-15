# sampling a sine wave programmatically
import numpy as np
import matplotlib.pyplot as plt
import time

# sampling information
Fs = 100000.0 # sample rate
T = 1/Fs # sampling period
t = 60.0 # seconds of sampling
N = Fs*t # total points in signal
print(N)

# signal information
#period = 2 ## seconds
freq =  1.0# in hertz, the desired natural frequency
omega = 2*np.pi*freq # angular frequency for sine waves

t_vec = np.arange(N)*T # time vector for plotting
y = np.sin(omega*t_vec)

plt.plot(t_vec,y)


# fourier transform and frequency domain
#
time_start = time.monotonic()
Y_k = np.fft.fft(y)[0:int(N/2)]/N # FFT function from numpy
time_end = time.monotonic()
print('Time Elapsed = ',time_end-time_start)
Y_k[1:] = 2*Y_k[1:] # need to take the single-sided spectrum only
Pxx = np.abs(Y_k) # be sure to get rid of imaginary part
f = Fs*np.arange((N/2))/N; # frequency vector

# plotting
fig,ax = plt.subplots()
plt.plot(f,Pxx,linewidth=5)
ax.set_xscale('log')
ax.set_yscale('log')
plt.ylabel('Amplitude')
plt.xlabel('Frequency [Hz]')
plt.show()
