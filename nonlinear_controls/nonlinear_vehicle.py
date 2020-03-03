import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
from mpl_toolkits.mplot3d import Axes3D

g = 32.2
mu = 0.1
A = mu*g
    
Cd = 0.2
S = 19.3
rho = 0.00238
mass = 2000./g
B = 0.5*rho*S*Cd/mass
    
r = 1.0
C = 1/(r*mass)

def sat(xdot):
    eps = 0.1
    if xdot > eps:
        return 1
    elif xdot < eps:
        return - 1
    else:
        slope = 2/eps
        return slope*xdot

def Harry_Potter_Magic_Controller(state):
    x = state[0]
    xdot = state[1]
    
    k = 5.
    beta = -k*xdot
    dt = (1/(C*available_shaft_torque(xdot)))*(B*xdot**2 + A*sat(xdot) - (x-10) + beta)
    
    return dt 

def Derivatives(state,t):
    x = state[0]
    xdot = state[1]    
    
    dt = Harry_Potter_Magic_Controller(state)
    
    xddot = -A*sat(xdot) - B*xdot**2 + C*dt*available_shaft_torque(xdot)
    return [xdot,xddot]

def available_shaft_torque(xdot):
    tau_min = 100.0
    tau_max = 175.0
    sig = 0.1
    xhat = xdot - 50.0
    tau = (tau_max-tau_min)*(np.exp(sig*xhat)/(np.exp(sig*xhat)+1)-0.5) + (tau_max+tau_min)/2
    return tau

##Plot the maximum shaft torque for debugging
xdot = np.linspace(0,117.33,1000) #117.33 ft/s is 80 mph
tau = available_shaft_torque(xdot)
plt.figure()
plt.plot(xdot,tau)
plt.xlabel('Speed (ft/s)')
plt.ylabel('Available Shaft Torque (ft-lbs)')
plt.grid()

###Plot V
x = np.linspace(0,20,100)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
xx, xxdot = np.meshgrid(x, xdot, sparse=False, indexing='ij')
V = 0.5*(xx-10)**2 + 0.5*xxdot**2
ax.plot_surface(xx,xxdot,V)

###Plot Vdot
Vdot = 0*V
rowctr = -1
colctr = 0
for xi in x:
    rowctr += 1
    colctr = 0
    for xdoti in xdot:
        state = [xi,xdoti]
        statedot  = Derivatives(state,0)
        xddoti = statedot[1]
        Vdot[rowctr][colctr] = (xi-10)*xdoti + xdoti*xddoti
        colctr += 1

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xx,xxdot,Vdot)

##Simulate with alternating initial conditions
x0 = 0
xdot0 = 0
state0 = [x0,xdot0]
tout = np.linspace(0,100,100)
stateout = integrate.odeint(Derivatives,state0,tout)

xout = stateout[:,0]

plt.figure()
plt.plot(tout,xout)


plt.show()