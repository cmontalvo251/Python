import control as ctl
import numpy as np
import matplotlib.pyplot as plt

a = 1/0.8
k = 90*a/1.28

G = ctl.tf([k],[1,a])
print(G)

tout = np.linspace(0,1.2,1000)

tout,yout = ctl.step_response(G)

plt.plot(tout,yout*1.28)
plt.show()