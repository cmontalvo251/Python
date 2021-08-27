###Import numpy and other modules
import numpy as np
import math as mt
import matplotlib.pyplot as plt

###Change the default fontsize
font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 11}
plt.rc('font', **font)

def C(F):
    return (F-32.)*5./9.

###Create a function. Doesn't need to be this hard but we just wanted to in class
def Tfun(tin,tauin):
    return 60.0*(1-np.exp(-(1/tauin)*tin))+30.0

###X axis is time using linspace
### Start stop number of data points
t = np.linspace(0,10,1000)
###Make first line
tau = 0.2
y = Tfun(t,tau)
###Second line
tau1 = 3.0
y1 = Tfun(t,tau1)
##Third one
tau2 = 8.0
y2 = Tfun(t,tau2)

##Plot both lines
plt.figure()
plt.plot(t,y,'tab:orange',label='tau='+str(tau))
plt.plot(t,y1,'b-',label='tau='+str(tau1))
plt.plot(t,y2,'g-',label='tau='+str(tau2))

###Make a titlte and labels
plt.title('Different Time Constant for Thermistors')
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (F)')

##Legends and a grid
plt.legend()
plt.grid()


##Plot both lines
plt.figure()
plt.plot(t,C(y),'tab:orange',label='tau='+str(tau))
plt.plot(t,C(y1),'b-',label='tau='+str(tau1))
plt.plot(t,C(y2),'g-',label='tau='+str(tau2))

###Make a titlte and labels
plt.title('Different Time Constant for Thermistors')
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (C)')

##Legends and a grid
plt.legend()
plt.grid()

###SHow it
plt.show()

