import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
##String line = time + "," + latitude + "," + longitude + "," + latitude_origin + "," + longitude_origin + "," + X + "," + Y + "," + D + "," + VX_display + "," + VY_display + "," + V_display + "," + gps_speed + "," + CalcBearing + "," + bearing + "," + elevation;
pdfhandle = PdfPages('plots.pdf')
data = np.loadtxt('DR/logCombined.txt',delimiter=',')

time = data[:,0]

#Let's fix time for combined files when time resets to zero
for i in range(1,len(time)):
    if time[i]<time[i-1]:
        time[i:] = time[i:]+time[i-1]-time[i]

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
pdfhandle.savefig()

#Plot X and Y in miles
plt.figure()
plt.plot(Y,X,'b-*')
plt.plot(Y[0],X[0],'rs')
plt.xlabel('Y (mi)')
plt.ylabel('X (mi)')
plt.grid()
pdfhandle.savefig()

##Plot distance traveled in miles
plt.figure()
plt.plot(time,D)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Distance Traveled (mi)')
pdfhandle.savefig()

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
pdfhandle.savefig()

##Plot heading
plt.figure()
plt.plot(time,calcheading,label='Calculated Heading')
plt.plot(time,gpsheading,label='Heading from GPS')
plt.xlabel('Time (sec)')
plt.ylabel('Heading (deg)')
plt.legend()
plt.grid()
pdfhandle.savefig()

##Plot elevation
try:
    print('Initial Elevation = ',elevation[0])
    plt.figure()
    plt.plot(time,elevation)
    plt.xlabel('Time (sec)')
    plt.ylabel('Elevation (ft)')
    plt.grid()
    pdfhandle.savefig()

    ##Let's also plot velocity on the y-axis and elevation on the x-axis
    plt.figure()
    plt.plot(Vgps,elevation,'b-')
    plt.xlabel('Velocity (mph)')
    plt.ylabel('Elevation (ft)')
    plt.grid()
    pdfhandle.savefig()

    #Let's make a 3D plot with lat/lon and elevation
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.colors as colors
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(longitude,latitude,elevation,'b-')
    #Let's make a for loop where we plot a data point in a color that is proportional to velocity
    cmap = plt.get_cmap('jet') 
    norm = colors.Normalize(vmin=min(Vgps), vmax=max(Vgps))
    for i in range(0,len(time),50): # Plot every 10th point
        this_color = cmap(norm(Vgps[i])) # Get color proportional to velocity
        ax.scatter(longitude[i],latitude[i],elevation[i],color=this_color)
    ax.set_xlabel('Longitude (deg)')
    ax.set_ylabel('Latitude (deg)')
    ax.set_zlabel('Elevation (ft)')
    plt.grid()
    pdfhandle.savefig()
except:
    pass
pdfhandle.close()
plt.show()