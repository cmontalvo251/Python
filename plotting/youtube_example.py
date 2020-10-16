#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

###MATLAB Code
#function[f0,g0]=compute_JD_and_Curl(Phi1,Phi2,h)
#[Phi1y,Phi1x]=gradient(Phi1,h);
#[Phi2y,Phi2x]=gradient(Phi2,h);
#f0=Phi1x.*Phi2y-Phi1y.*Phi2x;
#g0=Phi2x-Phi1y;
def compute_JD_and_Curl(Phi1,Phi2,h):
	Phi1y,Phi1x=np.gradient(Phi1,h)
	Phi2y,Phi2x=np.gradient(Phi2,h)
	f0 = Phi1x*Phi2y-Phi1y*Phi2x
	g0 = Phi2x-Phi1y

	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	ax.plot_surface(xx,yy,Phi1y)
	ax.set_title('Phi1y')

	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	ax.plot_surface(xx,yy,Phi2y)
	ax.set_title('Phi2y')

	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	ax.plot_surface(xx,yy,Phi1x)
	ax.set_title('Phi1x')

	fig = plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	ax.plot_surface(xx,yy,Phi2x)
	ax.set_title('Phi2x')

	return f0,g0

###Generate the x and y coordinates
h = 2.0
x = np.arange(-10,10,h)
y = np.arange(-10,10,h)
xx,yy = np.meshgrid(x,y)
#print(xx,yy)

###Generate Phi1 and Phi2
Phi1 = 2*(xx**2 + yy**2)
Phi2 = 10*(xx + yy)

##Make a new figure
fig = plt.figure()
###Make it projection 3d
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xx,yy,Phi1)

fig1 = plt.figure()
ax1 = fig1.add_subplot(111,projection='3d')
ax1.plot_surface(xx,yy,Phi2)

f0,g0 = compute_JD_and_Curl(Phi1,Phi2,h)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111,projection='3d')
ax2.plot_surface(xx,yy,f0)

fig3 = plt.figure()
ax3 = fig3.add_subplot(111,projection='3d')
ax3.plot_surface(xx,yy,g0)

plt.show()