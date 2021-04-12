import numpy as np
import matplotlib.pyplot as plt

cool = np.loadtxt('Cool_Down.txt')
#heat = np.loadtxt('Heat_Up.txt')

time0 = 76.0 ##This is how much I need to shift the plot to the left to have my graph start at t=0
time_cool = cool[:,0]-time0
temp_cool = cool[:,1]
plt.figure()
plt.plot(time_cool,temp_cool,'b*',label='Measured Data')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (C)')

TA = -8.0 ##where the graph settls
T0 = 26.8 ##this is where the graph starts

### Time_to_settle = 4.0/tau #where time to settle is the value within 2% ish
time_to_settle = 620.0
tau = 4.0/time_to_settle
print(tau)
t = np.linspace(0,np.max(time_cool),1000)
T = (TA-T0)*(1-np.exp(-tau*t)) +  T0

plt.plot(t,T,'r-',label='Numerical Fit')

plt.show()