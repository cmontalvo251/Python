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
data = np.loadtxt('Angle_vs_Time.csv',delimiter=',')
xdata = data[:,0]
ydata = data[:,1]
plt.plot(xdata,ydata,'b*',label='Experimental Data')

###Zeros poles and gains
# X = k / (s + c)
tau = 0.85
c = 1/tau
FVT = 90.
k = FVT*c
N = [k]
D = [1,c]
G = ctl.tf(N,D)
print(G)
tout = np.linspace(0,5.0,1000)
tout,yout = ctl.step_response(G,tout)
plt.plot(tout,yout,'g--',label='Simulation')
plt.xlabel('Time (sec)')
plt.ylabel('Degrees')
plt.legend()
plt.grid()
plt.show()
