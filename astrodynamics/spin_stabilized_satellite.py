import numpy as np
import matplotlib.pyplot as plt

pulse_duration = 40.0/1000.0
pulse_wait_duration = 60.0/1000.0
thrusters = 0
pulse_off_time = -pulse_wait_duration
pulse_on_time = 0.0
Number_of_Pulses = 0.0

def Thrusters(t):
    global thrusters,pulse_off_time,pulse_on_time,pulse_wait_duration,pulse_duration,Number_of_Pulses
    ###Thrusters
    
    ###Torque on the spacecraft
    #Model Pulse Jet Thrusters
    #Are thrusters currently on?
    if thrusters == 1:
        ##Thrusters are currently on
        ##Do we need to turn them off?
        if (t >= pulse_on_time + pulse_duration):
            thrusters = 0
            pulse_off_time = t
    else:
        #Thrusters are currently off
        #Can I turn them back on?
        if (t >= pulse_off_time + pulse_wait_duration):
            thrusters = 1.0
            pulse_on_time = t
            Number_of_Pulses+=1
    
    r = 1.0
    F = 4.0*50.0*thrusters
    Torque = np.asarray([0,r*F,0])
    return Torque

def Derivatives(state,t,Torque):
    rpy = state[3:6]
    w = state[0:3]
    ##Inertia Matrix
    Ixx = 10.0
    Iyy = Ixx
    Izz = 500.0
    Inertia = np.asarray([[Ixx,0,0],[0,Iyy,0],[0,0,Izz]])
    Inertia_Inv = np.asarray([[1/Ixx,0,0],[0,1/Iyy,0],[0,0,1/Izz]])
    
    dHdt = Torque - np.cross(w,np.matmul(Inertia,w))
    dwdt = np.matmul(Inertia_Inv,dHdt)
    
    #Kinematics
    phi = rpy[0]
    theta = rpy[1]
    psi = rpy[2]
    ctheta = np.cos(theta)
    cpsi = np.cos(psi)
    sphi = np.sin(phi)
    stheta = np.sin(theta)
    cphi = np.cos(phi)
    spsi = np.sin(psi)
    ttheta = np.tan(theta)
    J = np.asarray([[1.0,sphi*ttheta,cphi*ttheta],[0.0,cphi,-sphi],[0.0,sphi/ctheta,cphi/ctheta]])
    drpydt = np.matmul(J,w)
    
    return np.hstack([dwdt,drpydt])
    
    
####So now we integrate in odeint
tout = np.linspace(0,10,10000)
dt = tout[2]-tout[1]
stateout = np.zeros((6,len(tout)))

stateout[:,0] = np.asarray([0,0,2000./500.,0,0,0])

pulses = 0*tout

for ctr in range(0,len(tout)-1):
    ti = tout[ctr]
    statei = stateout[:,ctr]
    ###RK4
    Torque = Thrusters(ti)
    pulses[ctr] = thrusters
    dstate1 = Derivatives(statei,ti,Torque)
    dstate2 = Derivatives(statei+dstate1*dt/2.0,ti+dt/2.0,Torque)
    dstate3 = Derivatives(statei+dstate2*dt/2.0,ti+dt/2.0,Torque)
    dstate4 = Derivatives(statei+dstate3*dt,ti+dt,Torque)
    chi = (1.0/6.0)*(dstate1 + 2*dstate2 + 2*dstate3 + dstate4)
    stateout[:,ctr+1] = statei + dt*chi

print('Number of Pulses = ',Number_of_Pulses)

wout = stateout[0:3,:]
rp = stateout[3:5,:]

plt.figure()
plt.plot(tout,np.transpose(wout))
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Ang Vel (rad/s)')

plt.figure()
plt.plot(tout,np.transpose(rp))
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Roll,Pitch (rad)')

plt.figure()
plt.plot(tout,pulses)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Pulses')

plt.show()