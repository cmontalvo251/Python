import numpy as np
import matplotlib.pyplot as plt

#data = np.loadtxt('Cool_Down.txt')
data = np.loadtxt('Heat_Up.txt')

##USE THESE FOR COOL DOWN
#TA = -8.0 ##where the graph settls
#T0 = 26.8 ##this is where the graph starts
#time_to_settle = 620.0
#time0 = 76.0 ##This is how much I need to shift the plot to the left to have my graph start at t=0

##USE THESE FOR HEAT UP
TA = 25.0
T0 = -2.0
time_to_settle = 250.0
time0 = 3.0

time = data[:,0]-time0
temp = data[:,1]
plt.figure()
plt.plot(time,temp,'b*',label='Measured Data')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (C)')



tau = time_to_settle/4.0 ##This is the time constant
print('Time Constant = ',tau)
t = np.linspace(0,np.max(time),1000)
T = (TA-T0)*(1-np.exp(-(1/tau)*t)) +  T0

plt.plot(t,T,'r-',label='Numerical Fit')

plt.show()