###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import scipy.signal as S

##Create a function

def Derivatives(x,t):
    xdot = 5*np.cos(2*t)-7*x

    return xdot #zdot is my output

##Main script
plt.close("all")

#integrate for 10 seconds
tout = np.linspace(0,10,10000)
xinitial = 0.0
xout = I.odeint(Derivatives,xinitial,tout)

plt.plot(tout,xout,label='Odeint Toolbox')

##Analytic Solution
A = -35.0/53.0
B = -A
C = 5-7*B
x_analytic = A*np.exp(-7*tout) + B*np.cos(2*tout) + C/2.0*np.sin(2*tout)

line,=plt.plot(tout,x_analytic,label='Analytic Solution')
line.set_dashes([2,2])


###Zeros poles and gains
N,D = S.zpk2tf([0],[-7,2j,-2j],5)
sys = ctl.tf(N,D)
print sys

tout,yout = ctl.impulse_response(sys,tout)

line,=plt.plot(tout,yout,color='green',label='Control Toolbox')
line.set_dashes([3,3])

plt.legend()

plt.grid()
plt.show()