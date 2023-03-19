import numpy as np
import matplotlib.pyplot as plt

def sat(input,epsilon,scalefactor):
    if (input > epsilon):
        #//Right side of graph
        return scalefactor;
    elif (input < -epsilon):
        #//left side of graph
        return -scalefactor;
    else:
        #//Inside the boundary so interpolate
        return input/epsilon*scalefactor

x = np.linspace(-2,2,1000)
ysat = [sat(xi,0.5,1) for xi in x]

plt.figure()
plt.grid()
plt.plot(x,ysat,label='Saturation Function')
plt.plot(x,np.sign(x),label='Sign Function')
plt.legend()
plt.show()