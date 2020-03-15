import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import scipy.signal as S
import scipy.linalg as slin

GOL = ctl.tf([1],[1,3])

print(GOL)

k = -3.01
GCL = ctl.tf([k],[1,3+k])

tout = np.linspace(0,500,100)

tout,yout = ctl.step_response(GCL,tout)

plt.plot(tout,yout)
plt.show()