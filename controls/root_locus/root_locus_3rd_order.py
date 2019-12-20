import control as ctl
import numpy as np
import matplotlib.pyplot as plt

plt.grid()
tout = np.linspace(0,10,1000)
for kp in range(0,60):
    den = [1,6,8,kp]
    s = np.roots(den)
    plt.plot(np.real(s),np.imag(s),'b*')
    #print(s)
    print(kp)
    G = ctl.tf([kp],den)
    tout,yout = ctl.step_response(G,tout)
    #print(G)
    #plt.plot(tout,yout)
    plt.pause(0.1)