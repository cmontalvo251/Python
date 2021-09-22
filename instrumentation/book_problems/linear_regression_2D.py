import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data = np.loadtxt('array2d.txt')
x = data[:,0]
y = data[:,1]
z = data[:,2]

###Fit data
##Create Z = H*coefficients
H = np.transpose([x,x**2,y,y**2,x*y])
##Solve for coefficients
## coefficients = (H'*H)^(-1)*H'*Z
HH = np.matmul(np.transpose(H),H)
HHinv = np.linalg.inv(HH)
HZ = np.matmul(np.transpose(H),z)
c = np.matmul(HHinv,HZ)
print(c)

xsmooth = np.linspace(np.min(x),np.max(x),20)
ysmooth = np.linspace(np.min(y),np.max(y),20)
xx, yy = np.meshgrid(xsmooth, ysmooth, sparse=False)
#H = np.transpose([x,x**2,y,y**2,x*y])
zz = c[0]*xx + c[1]*xx**2 + c[2]*yy + c[3]*yy**2 + c[4]*xx*yy

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.scatter(x,y,z,'b*')
ax.plot_surface(xx,yy,zz)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
