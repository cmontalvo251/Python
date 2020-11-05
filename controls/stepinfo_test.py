import control as ctl
import numpy as np
import matplotlib.pyplot as plt
import controlsplots as cctl
import json

wn = 10.0
zeta = 0.5

tout = np.linspace(0,10,1000)

G = ctl.tf([wn**2],[1,2*zeta*wn,wn**2])

tout,yout = ctl.step_response(G,tout)

plt.plot(tout,yout)

info = cctl.step_info(G)

print(ctl.step_info(G))

plt.show()