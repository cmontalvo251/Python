import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

###Create some fictitious data
x1 = np.linspace(0,10,5)
y1 = np.linspace(0,10,5)
xdata = []
ydata = []
for x in x1:
    xdata = np.hstack((xdata,[x]*len(x1)))
    ydata = np.hstack((ydata,y1))
xdata = np.asarray(xdata)
ydata = np.asarray(ydata)
zdata = 0.5*xdata + -0.3*ydata + 2.4*xdata**2 + 8.6*ydata**2 + 1.6*xdata*ydata
#Pollute with noise
scale = np.max(zdata) - np.min(zdata)
for ctr in range(0,len(zdata)):
    zdata[ctr] += (-1 + random.random()*2)*scale*0.1

#fig = plt.figure()
#ax = fig.gca(projection='3d')
#ax.scatter(xdata,ydata,zdata,'b*')
#plt.show()
    
outarray = np.transpose(np.vstack((xdata,ydata,zdata)))
print(np.shape(outarray))
file = open("array2d.txt","w")
file.write(str(outarray))
file.close()


