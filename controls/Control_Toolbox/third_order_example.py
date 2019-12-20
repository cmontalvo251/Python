###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import scipy.signal as S
import scipy.linalg as slin

plt.close("all")

G_open_loop = ctl.tf([1],[1,1,0])

tout = np.linspace(0,100,1000)
tout,xout = ctl.step_response(G_open_loop,tout)

#plt.plot(tout,xout,'b-')
#plt.grid()
#plt.xlabel('Time (sec)')
#plt.ylabel('X')

##Let's close the loop
plt.figure()
for kp in np.linspace(0.01,10,100):
    print(kp)
    G_closed_loop = ctl.tf([kp],[1,3,2,kp])
    print(G_closed_loop)
    tout,xout = ctl.step_response(G_closed_loop,tout)
    plt.plot(tout,xout)
    
plt.xlabel('Time (sec)')
plt.ylabel('X')

plt.grid()
plt.show()