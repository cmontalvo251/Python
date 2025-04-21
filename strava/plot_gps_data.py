import numpy as np
import matplotlib.pyplot as plt
##String line = time + "," + latitude + "," + longitude + "," + latitude_origin + "," + longitude_origin + "," + X + "," + Y + "," + D + "," + VX_display + "," + VY_display + "," + V_display + "," + gps_speed + "," + CalcBearing + "," + bearing + "," + elevation;

data = np.loadtxt('log0.txt',delimiter=',')

time = data[:,0]
latitude = data[:,1]
longitude = data[:,2]
latO = data[:,3]
lonO = data[:,4]
X = data[:,5]
Y = data[:,6]
D = data[:,7]
VX = data[:,8]
VY = data[:,9]
V = data[:,10]
Vgps = data[:,11]
calcheading = data[:,12]
gpsheading = data[:,13]
try:
    elevation = data[:,14]
except:
    pass

##Plot Latitude and Longitude
fig,ax = plt.subplots()
ax.xaxis.get_major_formatter().set_useOffset(False)
ax.yaxis.get_major_formatter().set_useOffset(False)
plt.plot(longitude,latitude,'b-*')
plt.plot(longitude[0],latitude[0],'rs')
plt.xlabel('Longitude (deg)')
plt.ylabel('Latitude (deg)')
plt.grid()

#Plot X and Y in miles
plt.figure()
plt.plot(Y,X,'b-*')
plt.plot(Y[0],X[0],'rs')
plt.xlabel('Y (mi)')
plt.ylabel('X (mi)')
plt.grid()

##Plot distance traveled in miles
plt.figure()
plt.plot(time,D)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Distance Traveled (mi)')

##Plot all the velocites
plt.figure()
plt.plot(time,VX,label='VX Calculated')
plt.plot(time,VY,label='VY Calculated')
plt.plot(time,V,label='V Calculated')
plt.plot(time,Vgps,label='V GPS')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Velocity (mph)')
plt.legend()

##Plot heading
plt.figure()
plt.plot(time,calcheading,label='Calculated Heading')
plt.plot(time,gpsheading,label='Heading from GPS')
plt.xlabel('Time (sec)')
plt.ylabel('Heading (deg)')
plt.legend()
plt.grid()

##Plot elevation
try:
    print('Initial Elevation = ',elevation[0])
    plt.figure()
    plt.plot(time,elevation)
    plt.xlabel('Time (sec)')
    plt.ylabel('Elevation (ft)')
    plt.grid()
except:
    pass

plt.show()