###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as C
import scipy.signal as S

plt.close("all")

###Zeros poles and gains
##This is just zpk in MATLAB
N,D = S.zpk2tf([],[-0,0,-1,-1],1)
sys1 = C.tf(N,D)
print sys1

#Just linspace in MATLAB
tout = np.linspace(0,10,10000)
tout,yout = C.impulse_response(sys1,tout)
plt.plot(tout,yout,color='green',label='Control Toolbox')

###Analytic Solution
A = -2.0
B = 1.0
C = 2.0
D = 1.0
x_analytic = A + B*tout + C*np.exp(-tout) + D*tout*np.exp(-tout)
line,=plt.plot(tout,x_analytic,color='blue',label='Analytic')
line.set_dashes([2,2])

plt.grid()
plt.legend()
plt.show()