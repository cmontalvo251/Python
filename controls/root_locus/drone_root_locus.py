import control as ctl
import matplotlib.pyplot as plt
import numpy as np


G = ctl.tf([1],[0.0045,0,0])
print(G)

tout = np.linspace(0,1,1000)

tout,yout = ctl.step_response(G,tout)

plt.figure()
plt.plot(tout,yout)

K = 0.03
b = 25.
c = 10*15.

C = ctl.tf([K,K*b,K*c],[1,0])

GCL = C*G/(1+C*G)

tout,yout = ctl.step_response(GCL,tout)

plt.figure()
plt.plot(tout,yout)

ctl.rlocus(C*G)

plt.show()