import numpy as np
import matplotlib.pyplot as plt

###CONTROL ROUTINE
def Control(t,state):
    #Extract State Vector
    x = state[0]
    y = state[1]
    psi = state[2]
    xdot = state[3]
    ydot = state[4]
    psidot = state[5]
    
    ##Defaults
    delta_steer = 1500.0
    delta_throttle = 1400.0
    
    return delta_steer,delta_throttle

##DERIVATIVES ROUTINE
def Derivatives(t,state):
    ##EXTRACT OUR STATE VECTOR
    x = state[0]
    y = state[1]
    psi = state[2]
    xdot = state[3]
    ydot = state[4]
    psidot = state[5]
    
    ##Mass Properties
    mass = 1.0 #kg
    Inertia = 1.0 #kg-m^2
    
    ##Friction or Drag terms
    CR = 1.0
    CD = 1.0
    CV = 25.0
    
    ##CONTROL TERMS
    DS = 1.0/500.0
    DT = 0.025
    
    ##KINEMATICS
    u = xdot * np.cos(psi) + ydot * np.sin(psi)
    v = -xdot * np.sin(psi) + ydot * np.cos(psi)
    
    ##CONTROL ROUTINE
    delta_steer,delta_throttle = Control(t,state)
    
    ##Control Forces
    Steer_Moment = DS * (delta_steer - 1500)
    Throttle_Force = DT * (delta_throttle - 1000)
    
    ##Total Forces and Moments
    Moments = Steer_Moment - CR*psidot
    ForceXbody = Throttle_Force - CD*u
    ForceYbody = -CV*v
    ForceX = ForceXbody * np.cos(psi) - ForceYbody * np.sin(psi)
    ForceY = ForceXbody * np.sin(psi) + ForceYbody * np.cos(psi)
    
    ##Dynamics
    ##Translation Dynamics
    xddot = ForceX / mass
    yddot = ForceY / mass
    
    ##Rotational Dynamics
    psiddot = Moments / Inertia
    
    ##RETURN THE DERIVATIVE OF OUR STATE VECTOR
    dstatedt = np.array([xdot,ydot,psidot,xddot,yddot,psiddot])
    return dstatedt
    
    
##RUN SIMULATION
dt = 0.1
tout = np.arange(0,20,dt)
xout = 0*tout
yout = 0*tout
xdotout = 0*tout
ydotout = 0*tout
psiout = 0*tout
psidotout = 0*tout
ctr = 0
#Initial Conditions
x = 0.
y = 0.
xdot = 10.
ydot = 0.
psi = 0.
psidot = 0.
state0 = np.array([x,y,psi,xdot,ydot,psidot])
for t in tout:
    ##Save States
    xout[ctr] = state0[0]
    yout[ctr] = state0[1]
    psiout[ctr] = state0[2]
    xdotout[ctr] = state0[3]
    ydotout[ctr] = state0[4]
    psidotout[ctr] = state0[5]
    #RK4
    k1 = Derivatives(t,state0)
    k2 = Derivatives(t+dt/2,state0+k1*dt/2)
    k3 = Derivatives(t+dt/2,state0+k2*dt/2)
    k4 = Derivatives(t+dt,state0+k3*dt)
    phi = (1./6.)*(k1 + 2*k2 + 2*k3 + k4)
    state0 += phi*dt
    ctr+=1
    #print('T = ',t)

##PLOTS
plt.figure()
plt.plot(xout,yout)
plt.grid()
plt.xlabel('x')
plt.ylabel('y')

##Body Frame Velocity
uout = xdotout * np.cos(psiout) + ydotout * np.sin(psiout)
vout = -xdotout * np.sin(psiout) + ydotout * np.cos(psiout)
plt.figure()
plt.plot(tout,uout,label='U')
plt.plot(tout,vout,label='V')
plt.grid()
plt.legend()
plt.xlabel('t')
plt.ylabel('velocity')

plt.figure()
plt.plot(tout,psidotout)
plt.grid()
plt.xlabel('t')
plt.ylabel('Yaw Rate (rad/s)')

plt.show()