###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import scipy.signal as S
import scipy.linalg as slin


##Main script
plt.close("all")

#integrate for 10 seconds
tout = np.linspace(0,10,10000)

###Zeros poles and gains
# X = 15 / ((s^2+9) * (s^2 + 6s + 8) )
N,D = S.zpk2tf([],[-2,-4,-3j,3j],15)
sys = ctl.tf(N,D)
print(sys)
tout,yout = ctl.impulse_response(sys,tout)
plt.plot(tout,yout,'g-',label='Control Toolbox')

##Analytic Solution using Inverse Laplace
A = 15.0/26.0
B = -15.0/50.0
D = (15-36*A-18*B)/8.0
C = (15-50*A-30*B-15*D)/15.0
x_analytic_laplace = A*np.exp(-2*tout) + B*np.exp(-4*tout) + C*np.cos(3*tout) + D/3.0*np.sin(3*tout)
plt.plot(tout,x_analytic_laplace,'k--',label='Inverse Laplace')

plt.grid()
plt.legend()
plt.show()