import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci

def Derivatives(T,t):
    tau = 1.739 #1 divided by the time constant
    Tdot = -tau*T
    return Tdot

###Problem 10
Time = np.asarray([0,0.1,0.5,1,2,3])
Temperature = np.asarray([20,16.7,8.1,3.3,0.6,0.1])

Time_to_settle = 2.3
tau = 4.0/Time_to_settle
print('Time Constant = ',tau)

Time_fit = np.linspace(Time[0],Time[-1],100)
Temperature_fit = Temperature[0]*np.exp(-tau*Time_fit)

Temperature_scipy = sci.odeint(Derivatives,20.0,Time_fit)

plt.plot(Time,Temperature,'b*')
plt.plot(Time_fit,Temperature_fit,'r--')
plt.plot(Time_fit,Temperature_scipy,'g-.')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (C)')

plt.show()