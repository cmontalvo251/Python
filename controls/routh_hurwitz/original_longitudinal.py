import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S

def Derivatives(xvec,t):
    alfa = xvec[0]
    alfadot = xvec[1]
    h = xvec[2]
    hdot = xvec[3]

    #Outer Loop Control
    kp = 0.01
    kd = 0.05
    hc = 1.0
    hdotc = 0.0
    hddotc = 0.0
    alfac = kp*(hc - h) + kd*(hdotc - hdot) #is the key really just derivative gain?
    #alfadotc = kp*(hdotc - hdot) + kd*(hddotc - hddot) ##Not possible because hddot depends on de
    
    #alfac = 5*np.pi/180.0
    alfadotc = 0.0
    
    kp = 4.0
    kd = 4.0/3.0
    
    de = kp*(alfac-alfa) + kd*(alfadotc-alfadot)
    
    alfaddot = -4*alfa - 4*alfadot + 3*de
    
    hddot = 6*alfa - de
    
    xvecdot = np.asarray([alfadot,alfaddot,hdot,hddot])
    return xvecdot

plt.close("all")

tout = np.linspace(0,100,1000)
xinitial = np.asarray([0,0,0,0])
xout = S.odeint(Derivatives,xinitial,tout)

plt.plot(tout,xout[:,0]*180.0/np.pi,label='AoA')
plt.legend()
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Angle of Attack (deg)')

plt.figure()
plt.plot(tout,xout[:,2],label='Altitude')
plt.legend()
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Altitude (m)')

plt.show()
