import numpy as np
import matplotlib.pyplot as plt
##String line = time + "," + latitude + "," + longitude + "," + latitude_origin + "," + longitude_origin + "," + X + "," + Y + "," + D + "," + VX_display + "," + VY_display + "," + V_display + "," + gps_speed + "," + CalcBearing + "," + bearing;


data = np.loadtxt('log0.txt',delimiter=',')

time = data[:,0]
calcheading = data[:,12]
gpsheading = data[:,13]


plt.plot(time,calcheading)
plt.plot(time,gpsheading)
plt.grid()

plt.figure()
plt.plot(data[:,2],data[:,1])
plt.plot(data[0,2],data[0,1],'rs')

plt.show()