import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

###Create a model of your system. Either it's second order
###or first order like this
def Derivatives(T,t):
    ###The final temperature value
    Tc = 42
    ###Guess and check on this value
    ###until your simulation matches your data
    a = 0.1
    ##This is a model of your system.
    Tdot = -a*T + a*Tc
    
    return Tdot

###Generate some example data - This requires an experiment
tdata = np.asarray([0,5,10,15,20,25,30])
Tdata = np.asarray([70,60,52,45,42,42,42])

##Plot the data
plt.plot(tdata,Tdata,'b*')

##Simulate the model you created above
tout = np.linspace(0,30,1000)
Tout = S.odeint(Derivatives,70,tout)

###plot the simulation data
plt.plot(tout,Tout,'r-')

plt.show()