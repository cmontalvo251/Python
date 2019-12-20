###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as C
import scipy.signal as S

##Create a function

def Derivatives(xvec,t):
    x = xvec[0]
    theta = xvec[1]
    xdot = xvec[2]
    thetadot = xvec[3]
    
    F = 0
    m = 2.
    M = 5.
    g = 9.81
    l = 1.
    
    kp = 10.
    kd = 5.
    ##Lyapunov - Use this to stabilize theta
    F = (1./np.cos(theta))*(-10*thetadot-M*g*np.sin(theta) - g*m*np.sin(theta) + l*m*thetadot**2*np.sin(2*theta)/2. - np.sin(theta)*g*(M + m*np.sin(theta)**2)/l)
    #Lyapunov - Use this to stabilize X
    F = -g*m*np.sin(2*theta)/2.+l*m*thetadot**2*np.sin(theta)-x*(M+m*np.sin(theta)**2)-10*xdot
    #Lyapunov
    alfa = -g*m*np.sin(2*theta)/2. + l*m*thetadot**2*np.sin(theta)
    beta = (M+m*np.sin(theta)**2)
    eta = 1000*(m+M)
    gamma = eta*(M*xdot + l*m*thetadot*np.cos(theta))
    F = -alfa - gamma*beta
    
    thetaddot = (F*np.cos(theta) + M*g*np.sin(theta) + g*m*np.sin(theta) - l*m*thetadot**2*np.sin(2*theta)/2.)/(l*(M + m*np.sin(theta)**2))
    xddot = (F + m*l*thetaddot*np.cos(theta) - m*l*(thetadot**2)*np.sin(theta))/(M+m)

    xvecdot = np.asarray([xdot,thetadot,xddot,thetaddot])

    return xvecdot #zdot is my output

##Main script
plt.close("all")

#integrate for 10 seconds
tout = np.linspace(0,10,1000)
xinitial = np.asarray([1,np.pi/3.,0,0])
xout = I.odeint(Derivatives,xinitial,tout)
plt.plot(tout,xout[:,1])
plt.xlabel('Time(sec)')
plt.ylabel('Theta')

plt.figure()
plt.plot(tout,xout[:,0])
plt.xlabel('Time(sec)')
plt.ylabel('X')
plt.show()

