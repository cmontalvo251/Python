import numpy as np
import matplotlib.pyplot as plt
import control 

g = 9.81
L = 1.0
m = 5.0

b = 3.0

#C = K(s+b)
#G = (1/m*L^2)/(s^2 - g/L)

# s^2 - g/L + K/m*L^2 * (s+b)

k_vec = np.linspace(0,1000,1000)
for k in k_vec:
    roots = np.roots([1,k/(m*L**2),k/(m*L**2)*b-g/L])
    #print(roots)
    plt.plot(np.real(roots),np.imag(roots),'b*')
plt.show()

#L = s+2/ (s * (s-2))

#1 + K (s+2)/(s*(s-2))

#s*(s-2) + K*s + 2*k

#s^2 - 2*s + K*s + 2*k

