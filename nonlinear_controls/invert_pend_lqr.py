from control import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I

plt.close("all")

############################################################################
#FUNCTIONS SECTION

def control(state):
    
    x = state[0]
    theta = state[1]
    xdot = state[2]
    thetadot = state[3]
    
    #LINEARIZE SYSTEM ABOUT UPRIGHT EQUILIBRIUM POINT
    AL = [[0,0,1,0],[0,0,0,1],[0,-(M+m)*g/M,0,0],[0,-m*g/(M*L),0,0]]
    BL = [[0],[0],[1/M],[1/(M*L)]]
    
    #LINEAR QUAD. REG. FOR OPTIMAL GAIN MATRIX K
    q = 10.0
    Q = [[q,0,0,0],[0,q,0,0],[0,0,q,0],[0,0,0,q]]
    R = [0.01]
    K,S,E = lqr(AL,BL,Q,R) 
    
    #PID CONTROL LAW
    U_x = K[0][0]*(x_c-x) + K[0][2]*(xdot_c-xdot)
    U_theta = K[0][1]*(theta_c-theta) + K[0][3]*(thetadot_c-thetadot)
    U = U_x + U_theta
    
    #OPEN LOOP
    #U = 0.0

    return U

def derivatives_linear(state,t):
    
    FL = control(state)
    
    AL = np.asarray([[0,0,1,0],[0,0,0,1],[0,-(M+m)*g/M,0,0],[0,-m*g/(M*L),0,0]])
    BL = np.asarray([0,0,1/M,1/(M*L)])
    
    statedot = np.matmul(AL,state) + BL*FL
    
    return statedot

def derivatives(state,t):
    
    theta = state[1]
    xdot = state[2]
    thetadot = state[3]

    F = control(state)

    A = M+m
    B = -m*L*np.cos(theta)
    C = m*L*np.sin(theta)
    
    xddot = (1/(1+B/(L*A)*np.cos(theta)))*(F-B/L*g*np.sin(theta)-C*thetadot**2)
    thetaddot = (1/L)*((xddot*np.cos(theta))+(g*np.sin(theta)))

    statedot = np.asarray([xdot,thetadot,xddot,thetaddot])
    
    return statedot

#END FUNCTIONS SECTION
############################################################################



############################################################################
#VARIABLES SECTION

#PARAMETERS
M = 2.0 #mass of cart, kg
m = 0.5 #mass of pendulum end, kg
g = 9.81 #gravity, m/s^2
L = 1.0 #length of pendulum, m

#INITIAL CONDITIONS
x_init = 0.0 #cart position, m
theta_init = -np.pi/4 #pendulum angle, rad
xdot_init = 0.0 #cart velocity, m/s
thetadot_init = 0.0 #pendulum angular rate, rad/s
state_init = np.asarray([x_init,theta_init,xdot_init,thetadot_init])

#TIME SPAN TO INTEGRATE OVER
t_init = 0.0
t_final = 20.0
dt = 0.01
tspan = np.linspace(t_init,t_final,int(t_final/dt+1))

#COMMANDS
x_c = 0.0 #cart position, m
theta_c = 0.0 #pendulum angle, rad
xdot_c = 0.0 #cart velocity, m/s
thetadot_c = 0.0 #pendulum angular rate, rad/s

#END VARIABLES SECTION
############################################################################



############################################################################
#INTEGRATION SECTION

#INTEGRATE NON-LINEAR SYSTEM
state_out = I.odeint(derivatives,state_init,tspan)
x_out = state_out[:,0]
theta_out = state_out[:,1]
xdot_out = state_out[:,2]
thetadot_out = state_out[:,3]

#INTEGRATE LINEAR SYSTEM
stateL_out = I.odeint(derivatives_linear,state_init,tspan)
xL_out = stateL_out[:,0]
thetaL_out = stateL_out[:,1]
xdotL_out = stateL_out[:,2]
thetadotL_out = stateL_out[:,3]

#END INTEGRATION SECTION
############################################################################



############################################################################
#PLOTTING SECTION

#x
plt.figure()
plt.plot(tspan,x_out,label='Non-Linear')
#plt.plot(tspan,xL_out,label='Linear')
plt.xlabel('Time (sec)')
plt.ylabel('X (m)')
plt.grid()
#plt.legend()

#THETA
plt.figure()
plt.plot(tspan,theta_out*180/np.pi,label='Non-Linear')
#plt.plot(tspan,thetaL_out,label='Linear')
plt.xlabel('Time (sec)')
plt.ylabel('Theta (deg)')
plt.grid()
#plt.legend()
"""
#XDOT
plt.figure()
plt.plot(tspan,xdot_out,label='Non-Linear')
plt.plot(tspan,xdotL_out,label='Linear')
plt.xlabel('Time (sec)')
plt.ylabel('Xdot (m/s)')
plt.grid()
plt.legend()

#THETADOT
plt.figure()
plt.plot(tspan,thetadot_out,label='Non-Linear')
plt.plot(tspan,thetadotL_out,label='Linear')
plt.xlabel('Time (sec)')
plt.ylabel('Thetadot (rad/s)')
plt.grid()
plt.legend()
"""
plt.show()

#END PLOTTING SECTION
############################################################################