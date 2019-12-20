import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S
import control as C


plt.close("all")

##Constants
mu0 = 1000
kt = 0.00001
a1 = 50.0
m = 2.0
area = 1.0
CD = 0.05
rho = 1.225
vstar = 20
mustar = mu0 + np.sqrt(rho*vstar**2*area*CD/(2*kt*a1**2))
kp = 1.5
vc = 30
dvc = vc - vstar

def Derivatives(v,t):
    
    ##Controller
    dv = v - vstar
    e = dvc - dv
    dmu = kp*e
    mu = dmu + mustar
    
    ###Dynamics
    D = 0.5*rho*v**2*area*CD
    omega = a1*(mu-mu0)
    T = kt*omega**2
    vdot = (T-D)/m
    return vdot
    
tout = np.linspace(0,10,1000)
vinitial = vstar
vout = S.odeint(Derivatives,vinitial,tout)
plt.plot(tout,vout,label='Nonlinear System')

A = -rho*vstar*area*CD/m
B = 2*kt*a1**2*(mustar-mu0)/m
G_open_loop = C.tf([B],[1,-A])

G_closed_loop = kp*G_open_loop/(1+kp*G_open_loop) #assuming no sensor

tout,dvout = C.step_response(G_closed_loop,tout)
plt.plot(tout,dvc*dvout+vstar,'r--',label='Linear System')

plt.grid()

plt.xlabel('Time (sec)')
plt.ylabel('Velocity (m/s)')

plt.show()