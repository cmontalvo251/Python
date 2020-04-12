import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

###Create a model of your system. Either it's second order
###or first order like this
def Derivatives(T,t):
    ###The final temperature value
    Tc = 0
    ###Time constant
    tau = 9. ##seconds ##how long it takes to get to 68% of the final value
    a = 1/tau ##heat capacitance variable
    ##This is a model of your system.
    ## Tdot + a*T = a*Tc
    Tdot = -a*T + a*Tc
    
    return Tdot

###Generate some example data - This requires an experiment
tdata = np.asarray([0,5,10,15,20,25,30])
Tdata = np.asarray([70,60,52,45,42,42,42])-42

##Plot the data
plt.plot(tdata,Tdata,'b*')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (C)')

##Simulate the model you created above
tout = np.linspace(0,30,1000)
Tout = S.odeint(Derivatives,27.8,tout)

###plot the simulation data
plt.plot(tout,Tout,'r-')

plt.show()