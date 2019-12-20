import control as ctl
import matplotlib.pyplot as plt
import numpy as np

tau = 0.5

tau_more_juice = 0.18

sig = 1.0/tau
sig_mj = 1.0/tau_more_juice

G = ctl.tf([90*sig],[1,sig])
G_mj = ctl.tf([90*sig_mj],[1,sig_mj])

tout = np.linspace(0,4.0,100)

tout,yout = ctl.step_response(G,tout)
tout,yout_mj = ctl.step_response(G_mj,tout)

plt.plot(tout,yout)
plt.plot(tout,yout_mj,'r-')
plt.grid()
plt.show()