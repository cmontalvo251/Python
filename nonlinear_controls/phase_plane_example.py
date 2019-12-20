###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as C
import scipy.signal as S

##Create a function

def Derivatives(x,t):
    x1 = x[0] #Oh btw array start with 0 in python not 1 like MATLAb 
    x2 = x[1]
    
    x1dot = x2
    #xc = 0
    #xdotc = 0
    #kp = 50
    #kd = 30
    #u1 = -kp*(x1-xc) - kd*(x2 - xdotc)
    u1 = 0
    x2dot = -0.6*x2 - 3*x1 - x1**2 + u1
    #x2dot = -3*x1 - 0.6*x2
    #x2dot = 3*x1 - 0.6*x2

    xdot = np.asarray([x1dot,x2dot])

    return xdot #zdot is my output

##Main script
plt.close("all")

#integrate for 10 seconds
tout = np.linspace(0,10,10000)
x1initial = np.linspace(-10,10,30)
x2initial = np.linspace(-10,10,30)
for x1 in x1initial:
	for x2 in x2initial:
		x1eq = 0
		x2eq = 0
		xinitial = np.asarray([x1-x1eq,x2-x2eq])
		xout = I.odeint(Derivatives,xinitial,tout)

		x1out = xout[:,0] + x1eq
		x2out = xout[:,1] + x2eq

#A1 = np.asarray([[0,1],[-3,-0.6]])
#print A1
#A2 = np.asarray([[0,1],[3,-0.6]])
#print A2

#w1,v1 = np.linalg.eig(A1)
#print w1
#w2,v2 = np.linalg.eig(A2)
#print w2

#plt.plot(tout,x1out,label='x1')
#plt.plot(tout,x2out,label='x2')
#plt.grid()
#plt.legend()

#plt.figure()
		plt.plot(x1out,x2out)
plt.xlim([-10,10])
plt.ylim([-10,10])
plt.grid()
plt.show()