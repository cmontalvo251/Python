import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-10,10,100)

gamma = x
u = -x**3 - np.sin(x)**4 - gamma

xdot = x**3 + np.sin(x)**4 + u
###if x is small
### sin(x) ~= x
### xdot ~= -x**3 + x**4

plt.plot(x,xdot)
plt.grid()

###Create a Lyap Function
V = 0.5*x**2

plt.figure()
plt.plot(x,V)
plt.grid()

###Look at Vdot
plt.figure()
plt.plot(x,x*xdot)
plt.grid()

plt.show()