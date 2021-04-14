import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci

###Experimental Data
time = np.array([0.1,0.5,1,2,3])
temp = np.array([16.7,8.1,3.3,0.6,0.1])
plt.plot(time,temp,'b*',label='Experimental Data')

##Settling Time Guess

###Using the 98% value
tsettle = 2.0
tau = 4.0/tsettle 
#Tsettle (sec) = 4.0 / tau (sec^-1)

###Using the 68% value
#t68 = 0.6
#tau = 1.0/t68

time_constant = 1/tau
print(time_constant)

#This is Brigg's guess and he was right.
#tau = 1.0/time_constant #vat about dis? er....no.
###Analytic Solution
time_smooth = np.linspace(0,np.max(time),1000)
temp_analytic = temp[0]*np.exp(-tau*time_smooth)
plt.plot(time_smooth,temp_analytic,'r-',label='Analytic Solution')

##Numerical Solution
##First I need a derivatives routine
def Derivatives(T,t):
    Tdot = -tau*T
    return Tdot
##I need ot call the scipy.integration toolbox
Temperature_scipy = sci.odeint(Derivatives,temp[0],time_smooth)
plt.plot(time_smooth,Temperature_scipy,'c--',label='Numerical Solution')

plt.legend()
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Temp (C)')
plt.show()