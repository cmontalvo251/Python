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

###Hi-Tec Servo
# X = a / (s + a)
Ts = 0.2
a = 4/Ts
N = [a]
D = [1,a]
sys = ctl.tf(N,D)
print sys
tout = np.linspace(0,0.5,1000)
tout,yout = ctl.step_response(sys,tout)
plt.plot(tout,yout,'g-',label='Hi-Tec HS425')

####Spektrum Servo
Ts = 0.14
a = 4/Ts
N = [a]
D = [1,a]
sys = ctl.tf(N,D)
print sys
tout,yout = ctl.step_response(sys,tout)
plt.plot(tout,yout,color='orange',label='Spektrum Great')

plt.xlabel('Time (sec)')
plt.ylabel('Measured Windspeed (m/s)')
plt.legend()
plt.grid()
plt.show()