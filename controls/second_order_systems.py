import numpy as np
import matplotlib.pyplot as plt
import control as ctl
import scipy.integrate as sci

####PLOT THE ANALYTIC EQUATION
time = np.linspace(0,3,1000)
xA = 1-np.exp(-5*time)-5*time*np.exp(-5*time)

###SOLVE USING CONTROL TOOLBOX
G = ctl.tf([25],[1,10,25])
tout,xout = ctl.step_response(G,time)

###SOLVE USING ODEINT
def derivs(z,t):
    return [z[1],25.0 - 10.0*z[1] - 25*z[0]]
zout = sci.odeint(derivs, [0,0] , time)

###PLOT EVERYTHING
plt.figure()
plt.plot(time,xA,'b-',label='Analytic Solution')
plt.plot(time,xout,'r--',label='Control Toolbox Solution')
plt.plot(time,zout[:,0],'g-.',label='Odeint Toolbox Solution')
plt.xlabel('Time (sec)')
plt.ylabel('Position (m)')
plt.grid()
plt.legend()
plt.show()