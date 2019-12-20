import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

def Derivatives(zvec,t):
    z = zvec[0]
    zdot = zvec[1]
    
    m = 12.
    mhat = 1.
    g = 9.81
    z_d = 100
    zdot_d = 0
    zddot_d = 0
    ztilde = z - z_d
    ztildedot = zdot - zdot_d
    eta = 5.
    lam = 3.
    k = 12*(g + lam*ztildedot + eta)
    s = ztildedot + lam*ztilde
    #Boundary layer
    if s > 2:
        p = 1
    elif s < -2:
        p = -1
    else:
        p = s
    T = mhat*(g + zddot_d - lam*ztildedot - k*p)
    
    zddot = -g + T/m

    zvecdot = np.asarray([zdot,zddot])
    return zvecdot

plt.close("all")

tout = np.linspace(0,10,1000)
xinitial = np.asarray([0,0])
xout = S.odeint(Derivatives,xinitial,tout)
plt.plot(tout,xout[:,0])
plt.xlabel('Time(sec)')
plt.ylabel('Z(m)')
plt.grid()

plt.show()
