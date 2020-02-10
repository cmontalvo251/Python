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
data = np.loadtxt("Angle_vs_Time.csv",delimiter=',')
xdata = data[:,0]
ydata = 25*(data[:,1])/90. + 50.
plt.plot(xdata,ydata,'b*',label='Experimental Data')

###Zeros poles and gains
# X = k / (s + c)
tau = 0.45
c = 1/tau
FVT = 25.
k = FVT*c
N = [k]
D = [1,c]
G = ctl.tf(N,D)
print(G)
tout = np.linspace(0,5.0,1000)
tout,yout = ctl.step_response(G,tout)
plt.plot(tout,yout+50,'g--',label='Simulation')
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (deg)')
plt.legend()
plt.grid()
plt.show()

