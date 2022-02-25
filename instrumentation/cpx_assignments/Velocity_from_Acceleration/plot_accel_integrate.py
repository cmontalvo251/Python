import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('accel_car.txt')

t = data[:,0]

t -= t[0]  ##THIS MEAN TAKE t and substract t0 from the entire array

x = data[:,1]-1
y = data[:,2]
z = data[:,3] - 9.81

##Truncate
x = -x[t>10]
t = t[t>10]
t -= t[0]

##Digital Low Pass Complimentary Filter (Moving Average Filter, Linear 1D Kalman Filter)
xf = 0*x
xf[0] = x[0]
s = 0.8
for i in range(0,len(x)-1):
    xf[i+1] = s*xf[i] + (1-s)*x[i]
tf = t - 0.5
    
plt.plot(t,x,label='x')
plt.plot(tf,xf,label='xf')
#plt.plot(t,y,label='y')
#plt.plot(t,z,label='z')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Accel (m/s^2')
plt.legend()

###Integrate with a Reimman sum
vel = 0*x
for i in range(0,len(x)-1):
    vel[i+1] = vel[i] + xf[i]*(tf[i+1]-tf[i])
    
vel = 2.23*vel

plt.figure()
plt.plot(tf,vel)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Velocity (mph)')

plt.show()