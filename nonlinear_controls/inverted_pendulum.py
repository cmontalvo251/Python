import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import scipy.linalg as S

M = 2
m = 0.5
g = 9.81
L = 1.0
kp = 100.
kd = 50.
thetac = 0.0
thetadotc = 0.0
A = M+m
AL = np.asarray([[0,0,1,0],[0,0,0,1],[0,-(M+m)*g/M,0,0],[0,-m*g/(M*L),0,0]])
BL = np.asarray([0,0,1/M,1/(M*L)])
tspan = np.linspace(0,10,101)
xinitial = np.asarray([0.0001,-np.pi/8,0.0001,-0.0001]) #x theta xdot thetadot
dt = tspan[1]-tspan[0]
print(dt)
Adiscrete = np.eye(4) + dt*AL
eigs = np.linalg.eig(Adiscrete)
Bdiscrete = dt*BL
Cdiscrete = np.eye(4)

###Create our KCA and KCAB matrices
#KCA = [CA,CA^2,CA^3,...,CA^Hp]  # 4Hp x 4
#KCAB = CB along diagonal and then CAB CA^2B along the lower diagonals # 4Hp x 4Hp
#R = np.eye(Hp)*0 #Hp x Hp
#YC =  #4Hp x 1
#K = inv(KCAB^T * KCAB + R) * KCAB^T

def control(theta,thetadot):

    #PID
    F = -kp*(theta-thetac) - kd*(thetadot-thetadotc)

    ##Lyapunov
    B = -m*L*np.cos(theta)
    C = m*L*np.sin(theta)
    D = np.cos(theta)/L
    E = g*np.sin(theta)/L
    G = m*L**2*thetadot/(1+D*B/A)
    gam = 5*thetadot**2
    F = A/(G*D)*(G*D/A*C*thetadot**2-G*E-m*g*np.sin(theta)*thetadot-gam)

    ##MPC
    #U = K*(YC - KCA*state)
    
    return F

def DerivativesLinear(state,t):
    theta = state[1]
    thetadot = state[3]
    FL = control(theta,thetadot)
    
    statedot = np.matmul(AL,state) + BL*FL
    
    return statedot

def Derivatives(state,t):
    x = state[0]
    theta = state[1]
    xdot = state[2]
    thetadot = state[3]

    F = control(theta,thetadot)

    B = -m*L*np.cos(theta)
    C = m*L*np.sin(theta)
    D = np.cos(theta)/L
    E = g*np.sin(theta)/L
    G = m*L**2*thetadot/(1+D*B/A)
    xddot = (1/(1+B/(L*A)*np.cos(theta)))*(F-B/L*g*np.sin(theta)-C*thetadot**2)
    thetaddot = (1/L)*((xddot*np.cos(theta))+(g*np.sin(theta)))

    statedot = np.asarray([xdot,thetadot,xddot,thetaddot])
    return statedot

# main script
# integrate for 10 seconds
stateout = I.odeint(Derivatives,xinitial,tspan)
xout = stateout[:,0]
thetaout = stateout[:,1]
xdotout = stateout[:,2]
thetadotout = stateout[:,3]

##Integrate linear system
#tspan = np.linspace(0,10,100)
#xinitial = np.asarray([0.0001,-np.pi/12,0.0001,-0.0001]) #x theta xdot thetadot
stateoutL = I.odeint(DerivativesLinear,xinitial,tspan)
xoutL = stateoutL[:,0]
thetaoutL = stateoutL[:,1]
xdotoutL = stateoutL[:,2]
thetadotoutL = stateoutL[:,3]

##Discrete System

#Adiscrete = S.expm(A*dt)
#Ainv = np.linalg.inv(A)
#Bdiscrete = np.matmul(Ainv,np.matmul(Adiscrete-np.eye(4),B))
stateout_discrete = 0*stateout
stateout_discrete[0,:] = xinitial
for k in range(0,len(tspan)-1):
    theta = stateout_discrete[k,1]
    thetadot = stateout_discrete[k,3]
    FD = control(theta,thetadot)
    stateout_discrete[k+1,:] = np.matmul(Adiscrete,stateout_discrete[k,:]) + Bdiscrete*FD
    
stateout_discrete = np.asarray(stateout_discrete)
xoutD = stateout_discrete[:,0]
thetaoutD = stateout_discrete[:,1]
xdotoutD = stateout_discrete[:,2]
thetadotoutD = stateout_discrete[:,3]

#plot
plt.close("all")

#x
plt.figure()
plt.plot(tspan,xout)
plt.plot(tspan,xoutL)
plt.plot(tspan,xoutD)
plt.xlabel('Time (sec)')
plt.ylabel('X (m)')
plt.grid()
#theta
plt.figure()
plt.plot(tspan,thetaout)
plt.plot(tspan,thetaoutL)
plt.plot(tspan,thetaoutD)
plt.xlabel('Time (sec)')
plt.ylabel('Theta (rad)')
plt.grid()
#xdot
plt.figure()
plt.plot(tspan,xdotout)
plt.plot(tspan,xdotoutL)
plt.plot(tspan,xdotoutD)
plt.xlabel('Time (sec)')
plt.ylabel('Xdot (m/s)')
plt.grid()
#thetadot
plt.figure()
plt.plot(tspan,thetadotout)
plt.plot(tspan,thetadotoutL)
plt.plot(tspan,thetadotoutD)
plt.xlabel('Time (sec)')
plt.ylabel('Thetadot (rad/s)')
plt.grid()
plt.show()
