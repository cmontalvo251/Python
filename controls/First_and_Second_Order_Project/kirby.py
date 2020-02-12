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

###Experimental Data

data = np.loadtxt('/home/carlos/Desktop/data.csv',delimiter=',')
xdata = data[:,0]
ydata = data[:,1]

plt.plot(xdata,ydata,'b*',label='Experimental Data')

###Zeros poles and gains
#X = k / (s + c)
Ts = 220
c = 4.6/Ts
FVT = 236.9
k = FVT*c**2
N = [k]
D = [1,2*c,c**2]
G = ctl.tf(N,D)
print(G)
tout = np.linspace(0,250,1000)
tout,yout = ctl.step_response(G,tout)
plt.plot(tout,yout+76.1,'g--',label='Simulation')
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (F)')
plt.legend()
plt.grid()
plt.show()
