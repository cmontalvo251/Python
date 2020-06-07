import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from celluloid import Camera

time = np.linspace(0,10,1000)
theta = time*2*np.pi/10.
x = 5*np.cos(theta)
y = 5*np.sin(theta)
fig = plt.figure('3-D')
camera = Camera(fig)
ax = fig.add_subplot(111,projection='3d')

totalplottingpts = 10 ##this restricts us to a certain number of points

##So no we need the skip parameter
skip = int(np.float(len(time))/np.float(totalplottingpts))

def figparams(x,y):
	f = 1.1
	ax.set_xlim([np.min(x)*f,np.max(x)*f])
	ax.set_ylim([np.min(y)*f,np.max(y)*f])
	ax.set_zlim([-1,1])
	plt.grid()	

iplot = 0
for i in range(0,len(x)):
	if i > iplot:
		#plt.pause(0.01)
		#plt.cla()
		ax.scatter(x[i],y[i],0,s=20)
		#ax.set_title(np.round(time[i]))
		figparams(x,y)
		iplot+=skip
		print('Snap')
		camera.snap()
animation = camera.animate()
#animation.save('test3D.gif',writer='imagemagick')

plt.show()