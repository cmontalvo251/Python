import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as S
import control as ctl

plt.close("all")

time = np.arange(0,2.1,0.1)
Tether44in = np.asarray([360,
    340,
    295,
    215,
    135,
    30,
    -40,
    -100,
    -140,
    -165,
    -135,
    -95,
    -40,
    0,
    35,
    90,
    110,
    110,
    100,
    70,
    40])
    
# F = m*xddot --- sum of forces = mass * acceleration - Newton
# M  = J*thetaddot -- sum of moments = inertia * angular acceleration - Euler

# -k*theta - c*thetadot = J*thetaddot
# thetaddot + c/J*thetadot + k/J*theta = 0
# THETA*s^2 - s*theta(0) - thetadot(0) + c/J*THETA*s - c/J*theta(0) + k/J*THETA

# THETA (s^2 + c*s/J + k/J) = s*theta(0) + thetadot(0) + c/J*theta(0)

# THETA = (s*theta(0) + thetadot(0) + c/J*theta(0)) / ((s^2 + c*s/J + k/J))

# THETA = (s*theta(0) + thetadot(0) + chat*theta(0)) / ((s^2 + chat*s + khat))

zeta = 0.2
period = 1.65
wn = 2*np.pi/period

chat = 2*zeta*wn
khat = wn**2
sys = ctl.tf([360*wn**2],[1,chat,khat])
print(sys)

tout = np.linspace(0,2,1000)

[tout,yout] = ctl.step_response(sys,tout)

plt.plot(time,-(Tether44in-360),'bs',label='Experimental Data')
plt.plot(tout,yout,'r--',label='Simulation')

plt.grid()
    
plt.show()
    
    
