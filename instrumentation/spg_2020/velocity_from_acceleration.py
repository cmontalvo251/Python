import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Accelerate_Car_250_end.txt')
#Grab raw data
t = data[:,0]
x = data[:,1]
y = data[:,2]
z = data[:,3]

##Clip Data
xc = x[t>248]
yc = y[t>248]
zc = z[t>248]
tc = t[t>248]

##Shift Data
tc-=tc[0]
xc-=xc[0]
yc-=yc[0]
zc-=zc[0]

##Filter z-axis
zcf = 0*zc
s = 0.25
for ctr in range(0,len(zc)-1):
    zcf[ctr+1] = (1-s)*zcf[ctr] + s*zc[ctr]

plt.plot(tc,xc,label='X')
plt.plot(tc,yc,label='Y')
plt.plot(tc,zc,label='Z')
plt.plot(tc,zcf,label='Z_Filtered')
plt.grid()
plt.legend()
plt.xlabel('Time (sec)')
plt.ylabel('Acceleration (m/s^2)')


##Get proper acceleration
acceleration = -zcf

###Integrate
velocity = 0*acceleration
deltat = tc[1]-tc[0]
ctr = 0
for ctr in range(0,len(acceleration)-1):
    velocity[ctr+1] = velocity[ctr] + acceleration[ctr]*deltat
    
#Plot
plt.figure()
plt.plot(tc,velocity*2.23694)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Velocity (mph)')

plt.show()