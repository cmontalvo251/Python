import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,5,1000)

w0 = 2*np.pi
a0  = 2.5
#an = 0
f = 0*t + a0
for n in range(1,100):
    plt.clf()
    an = 0.0
    bn = 5.0/(n*np.pi) * (1.0 - np.cos(n*np.pi))
    f = f + an * np.cos(n*w0*t) + bn * np.sin(n*w0*t)
    plt.plot(t,f)
    plt.pause(0.0001)
    

plt.show()