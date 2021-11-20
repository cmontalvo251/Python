import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Long_Cable_High_Freq.txt',delimiter=',')
data_bad = np.loadtxt('Long_Cable_Low_Freq.txt',delimiter=',')

time_b = data_bad[:,0]
time_b-=time_b[0]
z_b = data_bad[:,1]

time = data[:,0]-18.19
z = data[:,1]
zf = data[:,2]

Td = 1.3
Ts = 30.0
z0 = (1.63+1.86)/2.0
s = 4.0/Ts
wd = 2*np.pi/Td
wn = np.sqrt(wd**2 + s**2)
g = 9.81
L = g/(wn**2)
print('Length (inches) = ',L*3.28*12)
tfit = np.linspace(0,10,1000)
zfit = z0*np.exp(-s*tfit)*np.cos(wd*tfit)-0.2

plt.plot(time,z,'b-*')
plt.plot(tfit,zfit,'r--')
plt.plot(time_b,z_b,'g-*')
#plt.plot(time,zf,'g-*')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Accel (m/s^2)')
#plt.xlim([0,10])
plt.show()
