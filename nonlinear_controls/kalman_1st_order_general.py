import numpy as np
import matplotlib.pyplot as plt

SensorPeriod = 1.0
lastSensorTime = -2*SensorPeriod
ftilde = -3.2

def sensor(x,t):
    global lastSensorTime
    if (t-lastSensorTime) > SensorPeriod:
        lastSensorTime = t
        v = 0.01*np.sin(100*t)
        y = x + v
        return y
    else:
        return -99
    
def control(xm,t):
    ##Control law - make sure to use the model estimate and not the actual truth signal
    xc = 1.0
    e = xc - xm
    kp = 0.2
    u = kp*e
    return u

def Covariance_Engine(t,p):
    global ftilde
    ##Code in your Covariance Dynamics
    # q = E[ww^T]
    q = 10.0
    pdot = ftilde*p + p*ftilde + q
    return pdot

def Physics_Engine(t,x,u):
    #Disturbance
    w = 0*np.sin(3*t)
    
    ##Code in your state dynamics
    xdot = -3*x + 4*u + w

    return xdot

def Model_Engine(t,xm,u):
    global ftilde
    ##Code in your model dynamics
    xmdot = ftilde*xm + 3.9*u
    
    return xmdot
    

##Setup time stuff
tinitial = 0
tfinal = 100
timestep = 0.01

#Then we can run the RK4 engine
t = tinitial
print('Begin RK4 Integrator')
x = 0.
xm = 0.
p = 0.
tout = np.arange(tinitial,tfinal,timestep)
xout = np.zeros((len(tout),1))
xmout = 0*xout
pout = 0*xout
uout = 0*tout
ctr = 0
tmeasure = []
ybarout = []
for ctr in range(0,len(tout)):
    
    ##Call the controller
    u = control(xm,t)
    
    #Save states for plotting
    xout[ctr] = x
    xmout[ctr] = xm
    pout[ctr] = p
    uout[ctr] = u
    
    ##Extract time
    t = tout[ctr]
    
    ##See if we have a new measurement?
    ybar = sensor(x,t)
    if (ybar != -99):
        ######Compute K
        #r = E[vv^T]
        r = 0.01
        K = p/(p+r)
        #Get a new model state
        xm = xm + K*(ybar-xm)
        #Get a new covariance
        p = (1-K)*p
        #Save the measurement
        ybarout.append(ybar)
        tmeasure.append(t)
        
    ##Integrate the Model Use RK4
    k1 = Physics_Engine(t,x,u)
    k2 = Physics_Engine(t+timestep/2.0,x+k1*timestep/2.0,u)
    k3 = Physics_Engine(t+timestep/2.0,x+k2*timestep/2.0,u)
    k4 = Physics_Engine(t+timestep,x+k3*timestep,u)
    phi = (1.0/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    #Step State
    x += phi*timestep
    
    ##Integrate the Model Use RK4
    k1 = Model_Engine(t,xm,u)
    k2 = Model_Engine(t+timestep/2.0,xm+k1*timestep/2.0,u)
    k3 = Model_Engine(t+timestep/2.0,xm+k2*timestep/2.0,u)
    k4 = Model_Engine(t+timestep,xm+k3*timestep,u)
    phi = (1.0/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    #Step State
    xm += phi*timestep
    
    ##Integrate the Model Use RK4
    k1 = Covariance_Engine(t,p)
    k2 = Covariance_Engine(t+timestep/2.0,p+k1*timestep/2.0)
    k3 = Covariance_Engine(t+timestep/2.0,p+k2*timestep/2.0)
    k4 = Covariance_Engine(t+timestep,p+k3*timestep)
    phi = (1.0/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    #Step State
    p += phi*timestep
    
    print('Time =',t)
    
print('RK4 Integration Complete')

plt.close("all")

#plot Everything
plt.figure()
plt.plot(tout,xout,label='State')
plt.plot(tout,xmout,label='Model')
plt.plot(tmeasure,ybarout,'b*',label='Sensor Measurement')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('State')
plt.legend()

plt.figure()
plt.plot(tout,pout)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Covariance')

plt.figure()
plt.plot(tout,uout)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Control Input')

plt.show()