import control as ctl
import matplotlib.pyplot as plt
import numpy as np
G = ctl.tf([1],[10,0,0])
print(G)
tout = np.linspace(0,100,1000)
tout,yout = ctl.step_response(G,tout)
plt.plot(tout,yout)
plt.ylabel('Theta (rad)')
plt.xlabel('Time (sec)')

kp = 10.0
GCL = (kp*G)/(1+kp*G)
print(GCL)

tout,yout_closed_loop = ctl.step_response(GCL,tout)

plt.figure()
plt.plot(tout,yout_closed_loop)

plt.show()