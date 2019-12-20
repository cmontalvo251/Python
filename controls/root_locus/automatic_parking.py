import numpy as np
import matplotlib.pyplot as plt
import control as ctl
import time

m = 100
b = 50

kpvec = np.linspace(0,100,100)
tout = np.linspace(0,100,1000)

for kp in kpvec:
    den = [m,b,kp]
    GCL = ctl.tf([kp],den)
    #print(GCL)
    roots = np.roots(den)
    #ctl.pzmap(GCL)
    print(roots)
    #time.sleep(0.1)
    tout,xout = ctl.step_response(GCL,tout)
    plt.plot(tout,xout)
plt.show()