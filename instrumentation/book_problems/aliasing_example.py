import numpy as np
import matplotlib.pyplot as plt

deltas = 0.0 #rad
Ls = 0.0 #rad
swath = 45*np.pi/180.0

az_deg = np.linspace(0,180,100)
az_rad = az_deg * np.pi/180.0

cosdtprime = np.cos(swath)*np.sin(deltas)+np.sin(swath)*np.cos(deltas)*np.cos(az_rad)
dtprime = np.arccos(cosdtprime)
dt = 90.0 - dtprime * 180.0/np.pi

dt_rad = dt*np.pi/180.0

cosdL = (np.cos(swath)-np.sin(deltas)*np.sin(dt_rad))/(np.cos(deltas)*np.cos(dt_rad))

dL = np.arccos(cosdL)*180/np.pi

dt_all = np.hstack((dt,dt[-1::-1]))
Lt_all = np.hstack((Ls-dL,Ls+dL))

plt.plot(Lt_all,dt_all)
plt.xlim([-180,180])
plt.ylim([-180,180])

plt.show()
