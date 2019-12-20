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

kp = 10.
kd = 2.
ki = 10.

sys = ctl.tf([3*kd,3*kp,3*ki],[1,(4+3*kd),(4+3*kp),3*ki])

print sys

tout = np.linspace(0,4,1000)
aflacommand = tout*0 + 1

tout,alfaout = ctl.step_response(sys,tout)

plt.plot(tout,alfaout)
plt.plot(tout,aflacommand)
plt.show()

alfass = 3*kp/(4+3*kp)
ess = 1.- alfass
print alfass,ess
