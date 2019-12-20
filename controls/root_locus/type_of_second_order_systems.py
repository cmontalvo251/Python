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
c_vec = np.linspace(0,625,100)
for c in c_vec:
    den = [1,c,625]
    poles = np.roots(den)
    print(poles)
    gain = den[2]
    wn = np.sqrt(den[2])
    #Ts = 4./abs(np.real(poles[0]))
    tout = np.linspace(0,1,1000)
    sys = ctl.tf(gain,den)
    print(sys)
    #tout,xout = ctl.step_response(sys,tout)
    #plt.plot(tout,xout)
    #plt.grid()
#[N,D] = S.zpk2tf([5],[-2,-3],[1])
#sys = ctl.tf(N,D)
#print(sys)

    #plt.figure()
    [p,z] = ctl.pzmap(sys,True)
    plt.grid()
    plt.plot(np.real(z),np.imag(z),'ro')
    plt.plot(np.real(p),np.imag(p),'bx',markersize=20)
    

plt.show()