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

###Alright let's do this
zeros = [-7]
poles = [-3j,3j]
gain = 5.
tout = np.linspace(0,2.5,1000)
num,den = S.zpk2tf(zeros,poles,gain)
sys = ctl.tf(num,den)
print(sys)
tout,xout = ctl.step_response(sys,tout)
plt.plot(tout,xout)
plt.grid()

plt.figure()
[p,z] = ctl.pzmap(sys,True)
plt.grid()
plt.plot(np.real(z),np.imag(z),'ro')
plt.plot(np.real(p),np.imag(p),'bx',markersize=20)
    
plt.show()