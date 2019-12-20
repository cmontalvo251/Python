import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

def Derivatives(state,t):
    alfa = state[0]
    alfadot = state[1]
    x = state[2]
    xdot = state[3]

    ##Outer Loop Plant
    xddot = alfa/3.0
    xdddot = alfadot/3.0
    
    #Get Altitude
    h = 14*x - 4*xdot - xddot
    hdot = 14*xdot - 4*xddot - xdddot
    #hddot = 14*xddot - 4*xdddot - xddddot #not possible.
    
    ##Outer Loop Control
    kp = 0.01
    kd = 0.05
    hc = 1.0
    hdotc = 0.0
    hddotc = 0.0
    alfac = kp*(hc - h) + kd*(hdotc - hdot)
    #alfadotc = kp*(hdotc - hdot) + kd*(hddotc - hddot)
    alfadotc = 0.0

    #if alfac > 10*np.pi/180.0:
    #    alfac = 10*np.pi/180.0
    #elif alfac < -10*np.pi/180.0:
    #    alfac = -10*np.pi/180.0
    
    ##Inner Loop Command
    #alfac = 5*np.pi/180.
    #alfadotc = 0.0
    
    kp = 4.0
    kd = 4.0/3.0
    
    de = kp*(alfac-alfa) + kd*(alfadotc-alfadot)
    
    #if de > 30*np.pi/180.0:
    #    de = 30*np.pi/180.0
    #elif de < -30*np.pi/180.0:
    #    de = -30*np.pi/180.0
    
    alfaddot = -4*alfa - 4*alfadot + 3*de
        
    xvecdot = np.asarray([alfadot,alfaddot,xdot,xddot])
    return xvecdot

plt.close("all")

tout = np.linspace(0,100,1000)
stateinitial = np.asarray([0,0,0,0])
stateout = S.odeint(Derivatives,stateinitial,tout)

plt.plot(tout,stateout[:,0]*180.0/np.pi,label='AoA')
plt.legend()
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Angle of Attack (deg)')

#Extract h
xout = stateout[:,2]
xdotout = stateout[:,3]
alfaout = stateout[:,0]
xddotout = alfaout/3.0
hout = 14*xout - 4*xdotout - xddotout

plt.figure()
plt.plot(tout,hout,label='Altitude')
plt.legend()
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Altitude (m)')

plt.show()