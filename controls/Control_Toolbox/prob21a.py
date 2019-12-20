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

####Zeros Poles and Gains
###Zeros are the roots of the numerator
####Poles are the roots of the denominator
####Gain is the leading coefficient of numerator/leading coefficient of the denominator
tout = np.linspace(0,10,1000)
#X1 = (2*s+1) / ((s+1)^2 + 1) 
#X2 = 2/(s^2+4)*((s+1)^2 + 1) 
zeros1 = -0.5
poles1 = [-1+1j,-1-1j]
gain1 = 2.0
[N1,D1] = S.zpk2tf(zeros1,poles1,gain1)
X1 = ctl.tf(N1,D1)
print X1

zeros2 = []
poles2 = [-1+1j,-1-1j,-2j,2j]
gain2 = 2.0
[N2,D2] = S.zpk2tf(zeros2,poles2,gain2)
X2 = ctl.tf(N2,D2)
print X2

X = X1 + X2

print X

tout,yout = ctl.impulse_response(X,tout)
plt.plot(tout,yout,'g-',label='Simulation')


###Analyticl solution
matrix = np.asarray([[0,2,0,4],[5,5,5,5],[-1,1,-5,5],[20,10,16,8]])
sol = np.asarray([2,2,2,2])

ABCD = np.matmul(np.linalg.inv(matrix),sol)

A = ABCD[0]
B = ABCD[1]
C = ABCD[2]
D = ABCD[3]

x1 = 2*np.exp(-tout)*np.cos(tout) - 2*np.exp(-tout)*np.sin(tout) + np.exp(-tout)*np.sin(tout)
x2 = A*np.cos(2*tout) + B/2.0*np.sin(2*tout) + C*np.exp(-tout)*np.cos(tout) - C*np.exp(-tout)*np.sin(tout) + D*np.exp(-tout)*np.sin(tout)

x = x1 + x2

plt.plot(tout,x,'r--',label='Analytic Solution')

plt.xlabel('Time (sec)')
plt.ylabel('x(t)')
plt.legend()
plt.grid()
plt.show()