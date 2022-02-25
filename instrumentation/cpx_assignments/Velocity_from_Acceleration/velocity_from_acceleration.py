import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Accel.txt')
#Grab raw data
t = data[:,0]
x = data[:,1]
y = data[:,2]
z = data[:,3]
#dt = 0.0125
#t = np.arange(0,12.1,dt)

##Clip Data
tclip = 0.0
xc = x[t>tclip]
yc = y[t>tclip]
zc = z[t>tclip]
tc = t[t>tclip]

##Shift Data
tc-=tc[0]
xc-=xc[0]
xc+=0.68
yc-=yc[0]
zc-=zc[0]

##Filter x-axis
xcf = 0*xc
s = 0.1
for ctr in range(0,len(xc)-1):
    xcf[ctr+1] = (1-s)*xcf[ctr] + s*xc[ctr]

plt.plot(tc,xc,label='X')
plt.plot(tc,yc,label='Y')
plt.plot(tc,zc,label='Z')
plt.plot(tc,xcf,label='X_Filtered')
plt.grid()
plt.legend()
plt.xlabel('Time (sec)')
plt.ylabel('Acceleration (m/s^2)')


##Get proper acceleration
acceleration = -xcf

###Integrate
velocity = 0*acceleration
deltat = tc[1]-tc[0]
for ctr in range(0,len(acceleration)-1):
    velocity[ctr+1] = velocity[ctr] + acceleration[ctr]*deltat
    
#Plot
plt.figure()
plt.plot(tc,velocity*2.23694)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Velocity (mph)')

###Integrate
position = 0*velocity
for ctr in range(0,len(velocity)-1):
    position[ctr+1] = position[ctr] + velocity[ctr]*deltat

plt.figure()
plt.plot(tc,position*3.28)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Position (ft)')

plt.figure()
plt.plot(tc[1:]-tc[0:-1])

plt.show()