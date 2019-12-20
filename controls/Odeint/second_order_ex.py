import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I

plt.close("all")

def Derivatives(z,t):
    x = z[0]
    xdot = z[1]
    
    xdbldot = 3*np.cos(t) - 5*xdot - 10*x
    
    return np.asarray([xdot,xdbldot])
    
#Numerical
tout = np.linspace(0,10,100)
zout = I.odeint(Derivatives,np.asarray([0,0]),tout)
xout = zout[:,0]


plt.plot(tout,xout,label='Numerical ODE')


#Analytical
mat = np.asarray([[1,0,1,0],[5,1,0,1],[10,5,1,0],[0,10,0,1]]);
sol = np.asarray([0,0,3,0]);
ABCD = np.matmul(np.linalg.inv(mat),sol)
A = ABCD[0]
B = ABCD[1]
C = ABCD[2]
D = ABCD[3]
a = 5.0/2.0
w = np.sqrt(15.0/4.0)
x_analytic = A*np.cos(tout) + B*np.sin(tout) + D/w*np.exp(-a*tout)*np.sin(w*tout) + C*np.exp(-a*tout)*np.cos(w*tout) - C*a/w*np.exp(-a*tout)*np.sin(w*tout)

line,=plt.plot(tout,x_analytic,color='red',label='Analytic')
line.set_dashes([2,2])


plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Position (m)')
plt.legend()
plt.show()