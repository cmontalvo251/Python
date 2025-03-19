import numpy as np
import matplotlib.pyplot as plt

Vo = 9.9
Vi = 90.
G = Vo/Vi
Ro = 10.0
Ri = 100000.

a = 8*G
b = Ro*G + 9*G*Ri - Ri
c = G*Ro*Ri

R2 = np.roots([a,b,c])
R1 = 8*R2
print(R2)
print(R1)

#####
R2 = np.linspace(1,2000,1000)
R1 = 8*R2
RA = Ro+R1
RB = (1/Ri + 1/R2)**(-1)
Vo = Vi*(RB/(RA+RB))
plt.plot(R2,Vo)

Voideal = 10.0
e = 100*(Voideal-Vo)/Voideal
print(np.min(e))
plt.figure()
plt.plot(R2,e)

plt.show()