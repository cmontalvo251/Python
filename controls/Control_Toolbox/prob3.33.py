import control as ctl
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as S

plt.close("all")

m = 20.
b = 36.7
k = 64.8
A = k
AG = ctl.tf([A/m],[1,b/m,k/m])

tout = np.linspace(0,10,100)

[tout,yout] = ctl.step_response(AG,tout)

plt.plot(tout,yout)
plt.grid()
plt.show()