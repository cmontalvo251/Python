import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

plt.close("all")

def Derivatives(z,t):
    alfa = z[0]
    alfadot = z[1]
    gamma = z[2]
    
    alfac = 5
    e = alfac - alfa
    kp = 20
    
    alfacdot = 0
    kd = 10
    edot = alfacdot - alfadot

    ki = 10

    u = kp*e + kd*edot + ki*gamma
    
    alfaddot = 3*u - 4*alfadot - 4*alfa
    gammadot = e
    
    zdot = np.asarray([alfadot,alfaddot,gammadot])
    
    return zdot
    

tout = np.linspace(0,30,1000)
zinitial = np.asarray([3,0,0])
zout = S.odeint(Derivatives,zinitial,tout)


plt.plot(tout,zout[:,0])

plt.show()