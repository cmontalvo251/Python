import numpy as np
import matplotlib.pyplot as plt

X = np.asarray([0,10,16,21,40,50])
Y = np.asarray([0,-5,7,20,11,0])

plt.plot(X,Y,'b-')
plt.grid()

r = np.sqrt((X[1::]-X[0:-1:])**2+(Y[1::]-Y[0:-1:])**2)
T = np.asarray([0,4,8,12,16,20])
dt = T[1::]-T[0:-1:]
print(r)
print(dt)
V = r/dt
print(V)
