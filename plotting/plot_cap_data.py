import numpy as np
import matplotlib.pyplot as plt

###Import Data - #This will not run unless you get the required simulated data
data = np.loadtxt('Example_Cap_Data.txt')

###Grab Time
time_data = data[:,0]
###Shift to t=0
time_data -= time_data[0]
##Cap Data
cap_data = data[:,1]

##Plot Cap Data
plt.plot(time_data,cap_data,'b*',label='CPX Data')
plt.xlabel('Time (sec)')
plt.ylabel('Cap Value')
plt.grid()

###Get simulated Data
time_sim = np.linspace(0,time_data[-1],1000)
A = cap_data[0] - cap_data[-1]
B = cap_data[-1]
Time_to_Settle = time_data[-1]
tau = 4/Time_to_Settle ##This is from Diff Eq.
cap_sim = A*np.exp(-tau*time_sim) + B

plt.plot(time_sim,cap_sim,'r-',label='Simulation')

plt.legend()
plt.show()