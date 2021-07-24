import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

##Kerbin Parameters
G = 6.6742*10**-11; #%%Gravitational constant
Mkerbin = 5.2915158*10**22 #
muKerbin = G*Mkerbin
Rkerbin = 600000. #meters

##True Anamoly
nu = np.linspace(0,2*np.pi,1000)
##Semi Major Axis of an 80 km parking orbit
alt_AGL = 80000.
rp = Rkerbin + alt_AGL
ra = Rkerbin + 12000000.
a = (ra+rp)/2.
##Eccentricity
e = (ra - rp)/(ra+rp)
print(e)
##inclination
i = 56.0*np.pi/180.0 ##Drew's random satellite he wants a just slightly over polar retrograde orbit
###Longitude of the Ascending Node
W = 45*np.pi/180.0
#Argument of the periaps
w = 0.

##plot in the orbital plane
###Phat and Qhat
p = a*(1-e**2)
r = p/(1+e*np.cos(nu))
xp = r*np.cos(nu)
yq = r*np.sin(nu)

###Rotate to Kerbin Centered Inertial Frame (KCI)
zr = 0*xp
TPI = np.asarray([[np.cos(W)*np.cos(w)-np.sin(W)*np.sin(w)*np.cos(i),-np.cos(W)*np.sin(w)-np.sin(W)*np.cos(w)*np.cos(i),np.sin(W)*np.sin(i)],
                 [np.sin(W)*np.cos(w)+np.cos(W)*np.sin(w)*np.cos(i),-np.sin(W)*np.sin(w)+np.cos(W)*np.cos(w)*np.cos(i),-np.cos(W)*np.sin(i)],
                 [np.sin(w)*np.sin(i),np.cos(w)*np.sin(i),np.cos(i)]])
xi = 0*xp
yj = 0*yq
zk = 0*zr
for x in range(0,len(xp)):
  xyzO = np.asarray([xp[x],yq[x],zr[x]]) ##3x1 vector
  xyzi = np.matmul((TPI),xyzO)
  xi[x] = xyzi[0]
  yj[x] = xyzi[1]
  zk[x] = xyzi[2]

###Now let's Compute Velocity
vx = np.sqrt(muKerbin/p)*(-np.sin(nu))
vy = np.sqrt(muKerbin/p)*(e+np.cos(nu))
vel = np.sqrt(vx**2 + vy**2)

####################COMPILE AND RUN THE FORTRAN CODE#############

#Compile the Code
import os
os.system('rm a.out')
os.system('gfortran kerbin_orbit.f90')
os.system('rm Output_File.txt')

#Run the Code
os.system('./a.out')

#Import the text file
fortran_data = np.loadtxt('Output_File.txt')
xpf = fortran_data[:,0]
yqf = fortran_data[:,1]
xif = fortran_data[:,2]
yjf = fortran_data[:,3]
zkf = fortran_data[:,4]
vxf = fortran_data[:,5]
vyf = fortran_data[:,6]
velf = fortran_data[:,7]
nuf = fortran_data[:,8]

####################PLOTS#####################3  
plt.plot(xp,yq,'r-',label='Python')
plt.plot(xpf,yqf,'g--',label='Fortran')
plt.plot(xp[0],yq[0],'r*',markersize=20)
theta = np.linspace(0,2*np.pi,100)
xkerbin = Rkerbin*np.cos(theta)
ykerbin = Rkerbin*np.sin(theta)
plt.plot(xkerbin,ykerbin,'b-')
plt.legend()
plt.grid()
plt.title('Orbital Plane')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
xsph = np.cos(u)*np.sin(v)
ysph = np.sin(u)*np.sin(v)
zsph = np.cos(v)
ax.plot_surface(Rkerbin*xsph,Rkerbin*ysph,Rkerbin*zsph,color='blue',zorder=1)
ax.plot(xi,yj,zk,'r-',zorder=0,label='Python')
ax.plot(xif,yjf,zkf,'g--',zorder=0,label='Fortran')
ax.scatter(xi[0],yj[0],zk[0],'r*',s=20)
plt.legend()

plt.figure()
plt.plot(nu,vx,'b-',label='Vx')
plt.plot(nuf,vxf,'r--',label='VxF')
plt.plot(nu,vy,'r-',label='Vy')
plt.plot(nuf,vyf,'g--',label='VyF')
plt.plot(nu,vel,'g-',label='V')
plt.plot(nuf,velf,'b--',label='VF')
plt.grid()
plt.xlabel('True Anomaly (rad)')
plt.ylabel('Velocity (m/s)')
plt.legend()
    
plt.show()

