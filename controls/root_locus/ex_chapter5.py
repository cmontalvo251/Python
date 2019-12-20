import numpy as np
import matplotlib.pyplot as plt
k_vec = np.linspace(0,10,1000)
for k in k_vec:
    roots = np.roots([1,k,4,k])
    #print(roots)
    plt.plot(np.real(roots),np.imag(roots),'b*')
plt.show()

#L = s+2/ (s * (s-2))

#1 + K (s+2)/(s*(s-2))

#s*(s-2) + K*s + 2*k

#s^2 - 2*s + K*s + 2*k

