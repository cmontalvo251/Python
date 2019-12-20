###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import scipy.signal as S
import scipy.linalg as slin

plt.close("all")

zeta = 1
sig = 2.0
Ts = 4.6/sig
G_alfa = ctl.tf([3],[1,4,4])

tout = np.linspace(0,2*Ts,1000)
tout,xout = ctl.step_response(G_alfa,tout)
plt.plot(tout,xout)
plt.xlabel('Time (sec)')
plt.ylabel('Alfa')
plt.grid()


G_alt_alfa_input = ctl.tf([-1,-4,+14],[3,0,0])
#print(G_alt)

tout = np.linspace(0,10,1000)
tout,hout = ctl.step_response(G_alt_alfa_input,tout)
plt.figure()
plt.plot(tout,hout)
plt.xlabel('Time (sec)')
plt.ylabel('Altitude with Alfa input')
plt.grid()

G_alt_elev_input = ctl.tf([-1,-4,14],[1,4,4,0,0])
print(G_alt_elev_input)

tout = np.linspace(0,10,1000)
tout,hout = ctl.step_response(G_alt_elev_input,tout)
plt.figure()
plt.plot(tout,hout)
plt.xlabel('Time (sec)')
plt.ylabel('Altitude with Elev input')
plt.grid()

### C = kp + kd*s

## GCL = GC/(1+GC)

kp = 100.0
kd = 10.0

Gprime = ctl.tf([3*kd,3*kp],[1,4,4])
print(Gprime)

GCL = Gprime/(1+Gprime)
print(GCL)

tout = np.linspace(0,2*Ts,1000)
tout,alfa_cl_out = ctl.step_response(GCL,tout)
plt.figure()
plt.plot(tout,alfa_cl_out)
plt.xlabel('Time (sec)')
plt.ylabel('Alfa CL out')
plt.grid()

####
K = 16.0/3.0+0.01
tout = np.linspace(0,5,100)
GCL_w_3K = ctl.tf([3*K],[1,4,4,3*K])
tout,alfa_out = ctl.step_response(GCL_w_3K)
plt.figure()
plt.plot(tout,alfa_out)
plt.xlabel('Time (sec)')
plt.ylabel('Alfa w 3K')
plt.grid()



plt.show()