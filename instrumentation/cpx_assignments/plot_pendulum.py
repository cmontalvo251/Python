import numpy as np
import matplotlib.pyplot as plt

angle_bias = 8.78
angle = np.loadtxt('Example_Pendulum_Data.txt')-angle_bias
tshift = 0.526
time = np.arange(0,0.01*len(angle),0.01)-tshift
plt.plot(time,angle,'b*',label='Measured Data')
plt.xlabel('Time (sec)')
plt.ylabel('Angle (deg)')
plt.grid()

##Simulated data
t0 = tshift
t1 = 0.951
Ts = 1.8
theta0 = 34.388-angle_bias
time_sim = np.linspace(0,Ts,1000)
sigma = 4/Ts
T = t1 - t0
wd = 2*np.pi/T
print('wd = ',wd)
print('Sigma = ',sigma)
wn = np.sqrt(wd**2+sigma**2)
print('wn = ',wn)
L = (9.81/wn**2)*3.28*12
print('L (inches) = ',L)
theta_sim = theta0*np.exp(-sigma*time_sim)*np.cos(wd*time_sim)
plt.plot(time_sim,theta_sim,'r-',label='Fitted Data')
plt.legend()
plt.show()