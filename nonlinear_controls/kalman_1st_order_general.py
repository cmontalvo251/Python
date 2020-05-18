import numpy as np
import matplotlib.pyplot as plt

S = 0.6
rho = 1.225
SensorPeriod = 10
lastSensorTime = -2*SensorPeriod

def sensor(x,t):
    global lastSensorTime
    if (t-lastSensorTime) > SensorPeriod:
        lastSensorTime = t
        y = x + 0.1*np.sin(100*t)
        return y
    else:
        return -99
    
def control(state,t):
    ##Control law - make sure to use the model estimate and not the actual truth signal
    xm = state[1]
    xc = 1.0
    e = xc - xm
    u = 0.
    return u

def Physics_Engine(t,state,u):
    x = state[0]
    xm = state[1]
    p = state[2]
    
    ##Code in your model dynamics
    xmdot = 0.
        
    #Disturbance
    w = 0.
    
    ##Code in your state dynamics
    xdot = 0.
    
    ##Code in your Covariance Dynamics
    pdot = 0.
    
    statedot = np.asarray([xdot,xmdot,pdot])
    return statedot

##Setup time stuff
tinitial = 0
tfinal = 100
timestep = 0.1

#Then we can run the RK4 engine
t = tinitial
print('Begin RK4 Integrator')
x0 = 0.
xm0 = 0.
p0 = 0.
state = np.asarray([x0,xm0,p0])
tout = np.arange(tinitial,tfinal,timestep)
stateout = np.zeros((len(tout),len(state)))
uout = 0*tout
ctr = 0
tmeasure = []
ybarout = []
for ctr in range(0,len(tout)):
    
    ##Call the controller
    u = control(state,t)
    
    #Save states for plotting
    stateout[ctr,:] = state
    uout[ctr] = u
    
    ##Extract time
    t = tout[ctr]
    
    ##See if we have a new measurement?
    y = sensor(state[0],t)
    if (y != -99):
        ybar = y
        ######Compute K
        K = 0.
        #Get a new model state
        state[0] = state[0] + K*(ybar-state[1])
        #Get a new covariance
        state[2] = (1-K)*state[2]
        #Save the measurement
        ybarout.append(ybar)
        tmeasure.append(t)
        
    ##Integrate the Model Use RK4
    k1 = Physics_Engine(t,state,u)
    k2 = Physics_Engine(t+timestep/2.0,state+k1*timestep/2.0,u)
    k3 = Physics_Engine(t+timestep/2.0,state+k2*timestep/2.0,u)
    k4 = Physics_Engine(t+timestep,state+k3*timestep,u)
    phi = (1.0/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    #Step State
    state += phi*timestep
    print('Time =',t)
    
print('RK4 Integration Complete')

#plot Everything
plt.figure()
plt.plot(tout,stateout[:,0],label='State')
plt.plot(tout,stateout[:,1],label='Model')
plt.plot(tmeasure,ybarout,'b*',label='Sensor Measurement')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('State')
plt.legend()

plt.figure()
plt.plot(tout,uout)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Control Input')

plt.show()