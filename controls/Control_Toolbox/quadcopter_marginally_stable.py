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

###Zeros poles and gains
Ts = 0.2
zed = 1.0
wn = 4/(zed*Ts)
l = (7./12.)/3.28
m = 0.650
J = m*l**2/12.
kp = (wn**2)*J/(2*l)
kd = zed*J*wn/l ###This will give you a critically damped system
kd = 0.01 ###This will give you an underdamped system

sys = ctl.tf([2*l/J*kd,2*l/J*kp],[1.,2*l*kd/J,2*l*kp/J])
print sys
tout = np.linspace(0,2,1000)
tout,yout = ctl.step_response(sys,tout)

plt.plot(tout,yout,'g--',label='Step Response')
plt.xlabel('Time (sec)')
plt.ylabel('Angle (rad)')
plt.legend()
plt.grid()
plt.show()