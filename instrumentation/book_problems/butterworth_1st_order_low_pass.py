import numpy as np
import matplotlib.pyplot as plt
G0 = 1.0
C = 1.0e-6
R2 = 1.0
fc = 1/(2*np.pi*C*R2)
print('Corner Frequency = ',fc)
f = np.linspace(0,10*fc,1000)
mag = 1/(np.sqrt(1 + (2*np.pi*f*C*R2)**2))
dB = 20*np.log10(mag)

plt.plot(np.log10(f/fc),dB)
#plt.ylim([-100,1])

plt.figure()
phase = -np.arctan(f/fc)*180.0/np.pi
plt.plot(np.log10(f/fc),phase)

plt.show()