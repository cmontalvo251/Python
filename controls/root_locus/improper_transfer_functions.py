import numpy as np
import matplotlib.pyplot as plt
import control as ctl

k = np.arange(0.01,100,0.1)

num = [1,1,2]

G = ctl.tf(num,[1])
print(G)
GCL = G/(1+G)
print(GCL)

zeros = np.roots(num)
print('Zeros = ',zeros)

plt.plot(np.real(zeros),np.imag(zeros),'bo')

preal = []
pimag = []

for ki in k:
    den = [ki,ki,2*ki+1]
    #print(den)
    poles = np.roots(den)
    preal.append(np.real(poles))
    pimag.append(np.imag(poles))
plt.grid()
plt.plot(preal,pimag)
plt.plot(preal[0],pimag[0],'rx') #Plot first point. 
plt.show()
    