import mymath as M
import numpy as np

##Create a half circle
N = 1000
t = np.linspace(-1.0,1.0,N)
x = np.sqrt(1-t**2)

##Integrate using a Reimann Sum
half_pi = M.Reimmann(x,t)
print('Approximation using ',N,' discretizations')
print('Half Pi ~= ',half_pi)
print('Pi ~= ',2.0*half_pi)