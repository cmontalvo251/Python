import matplotlib.pyplot as plt
import numpy as np
from celluloid import Camera

time = np.linspace(0,10,1000)
theta = time*2*np.pi/10.
x = 5*np.cos(theta)
y = 5*np.sin(theta)

totalplottingpts = 50 ##this restricts us to a certain number of points

##So no we need the skip parameter
skip = int(np.float(len(time))/np.float(totalplottingpts))
fig = plt.figure()
camera = Camera(fig)
def figparams(x,y):
	f = 1.1
	plt.xlim([np.min(x)*f,np.max(x)*f])
	plt.ylim([np.min(y)*f,np.max(y)*f])
	plt.grid()	

iplot = 0
for i in range(0,len(x)):
	if i > iplot:
		#plt.pause(0.01)
		#plt.clf()
		plt.plot(x[i],y[i],'bs',markerSize=10)
		#plt.title(np.round(time[i]))
		figparams(x,y)
		iplot+=skip
		camera.snap()

animation = camera.animate()
animation.save('test.gif',writer='imagemagick')