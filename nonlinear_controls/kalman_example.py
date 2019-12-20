import numpy as np
import matplotlib.pyplot as plt
import random

S = 0.6
rho = 1.225
GPSperiod = 10
lastGPStime = -2*GPSperiod

def GPS(V,t):
    global lastGPStime
    if (t-lastGPStime) > GPSperiod:
        lastGPStime = t
        return V + random.randint(-10,10)
    else:
        return -99

def Physics_Engine(t,V,mu):
    m = 5.2
    CD = 0.3
    a0 = 1100.
    kt = 4e-5
    T = kt*(mu-a0)**2
    Vdot = T/m - 0.5*rho*V**2*S*CD/m
    return Vdot

##Setup time stuff
tinitial = 0
tfinal = 100
timestep = 0.1

#Then we can run the RK4 engine
t = tinitial
print('Begin RK4 Integrator')
V = 0. ##initial condition for velocity
V_out = []
Vhat_out = []
t_out = []
mu_out = []
while t <= tfinal:
    ################MICROCONTROLLER################
    
    ##See if we have a new measurement?
    Vnew = GPS(V,t)
    if (Vnew != -99):
        Vhat = Vnew
        #Run the Kalman Update
        #Compute K
        #Run the update
        #Get a new model state
        #Get a new covariance
        #Compute the new equilibrium throttle position
        #Compute your new A and B matrices
        #Compute G,F,H
        
    #Compute Control
    V_command = 10.0
    kp = 117.0
    ##Once your model integration is working you need to change Vhat to Vmodel
    mu = kp*(V_command+4 - Vhat) + 1100
    if (mu < 1100):
        mu = 1100
    elif (mu > 1900):
        mu = 1900
        
    ##Integrate the Model Use RK4
    ##Integrate the covariance using RK4    
    
    ###############################################
    
    
    #RK4 Call for Physics Engine (DO NOT TOUCH)
    k1 = Physics_Engine(t,V,mu)
    k2 = Physics_Engine(t+timestep/2.0,V+k1*timestep/2.0,mu)
    k3 = Physics_Engine(t+timestep/2.0,V+k2*timestep/2.0,mu)
    k4 = Physics_Engine(t+timestep,V+k3*timestep,mu)
    phi = (1.0/6.0)*(k1 + 2*k2 + 2*k3 + k4)
    #Combine States
    V_out.append(V)
    t_out.append(t)
    Vhat_out.append(Vhat)
    mu_out.append(mu)
    #Step State
    V += phi*timestep
    t+=timestep
    print('Time =',t)
    
print('RK4 Integration Complete')

#plot Everything
plt.figure()
plt.plot(t_out,V_out,label='Truth')
plt.plot(t_out,Vhat_out,'r-',label='Measured Data')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('V (m/s)')
plt.legend()

plt.figure()
plt.plot(t_out,mu_out)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Control Input (us)')

plt.show()