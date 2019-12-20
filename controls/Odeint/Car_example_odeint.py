import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

plt.close("all")

kp = 0.0

def Derivatives(v,t):
    m = 2000.0 #kilograms
    b = 2000.0 ##straight guess
    vc = 20.0 # m/s
    
    ##Stopped at a light
    u = 0.0 ##Newton
    ##Light turns green
    u = 80000.0 ##Straight guess
    if u > 50000.0:
        u = 50000.0
    ##Control system
    u = kp*(vc - v)
    ##drag = b*v --- Newtons = kg m/s^2 = kg/s * m/s
    vdot = u/m - b/m*v
    return vdot
    
tout = np.linspace(0,10,1000)
vinitial = 0.0

for idx in range(0,100):
    vout = S.odeint(Derivatives,vinitial,tout)
    plt.plot(tout,vout)
    kp+=1000.0
plt.xlabel('Time (sec)')
plt.ylabel('Velocity (m/s)')
plt.grid()
plt.show()