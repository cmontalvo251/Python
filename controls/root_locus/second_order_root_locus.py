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

plt.rcParams.update({'font.size': 18})

###Open Loop
den = [1,0,2]
poles = np.roots(den)
print(poles)
gain = 3.
wn = np.sqrt(2)
period = 2*np.pi/(wn)
sys = ctl.tf(gain,den)
print(sys)

plt.figure()
[p,z] = ctl.pzmap(sys,True)
plt.grid()
plt.plot(np.real(z),np.imag(z),'ro')
plt.plot(np.real(p),np.imag(p),'bx',markersize=20)

tout = np.linspace(0,2*period,1000)
tout,xout = ctl.step_response(sys,tout)
plt.figure()
plt.plot(tout,xout)
plt.grid()

##Close the loop
G = sys
print(G)
k1 = 5.
k2 = 2.5
plt.figure()
#for k in k_vec:
#cascadeG = k*G
##Don't do this. Just solve it by hand.
#GCL = cascadeG/(1+cascadeG)
GCL = ctl.tf([3*k2,3*k1],[1,k2,2+3*k1])
print(GCL)

#[p,z] = ctl.pzmap(GCL,True)
#plt.grid()
#plt.plot(np.real(z),np.imag(z),'ro')
#plt.plot(np.real(p),np.imag(p),'bx',markersize=20)
tout = np.linspace(0,2*period,1000)
tout,xout = ctl.step_response(GCL,tout)
plt.plot(tout,xout)
#plt.grid()


plt.show()
