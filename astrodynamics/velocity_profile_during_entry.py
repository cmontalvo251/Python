import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I


###Compiute Angular Velocity
#w_deg_per_hr = 360./23.9344696
#w_rad_per_s = (w_deg_per_hr * np.pi/180.0 ) * (1.0/3600.)
#print(w_rad_per_s)

##Altitude =
h = np.linspace(0,122000,100000) #100 km
Ve = 7500.0 #m/s
beta = 0.1354/1000.0 ##density constant
rhos = 1.225 #kg/m^3
m = 1350.0 #kg
CD = 1.5 #unitless - non dimensional coefficient
S = 2.8 #m^2 - planform area of entry vehicle

gamma = -40*np.pi/180.0
V = Ve*np.exp((1.0/(2*beta))*(rhos/(np.sin(gamma)))*(S*CD/m)*np.exp(-beta*h))

###Compute Acceleration
drdt = V*np.sin(gamma)
dhdt = drdt
dVdh = (V[0:-2]-V[1:-1])/(h[0:-2]-h[1:-1])
accel = dVdh*dhdt[0:-2]

plt.figure()
plt.plot(h,V)
plt.xlabel('Altitude (m)')
plt.ylabel('Velocity (m/s)')
plt.grid()


plt.figure()
plt.plot(h[0:-2],accel/9.81)
plt.xlabel('Time (sec)')
plt.ylabel('Gs')
plt.grid()

plt.show()