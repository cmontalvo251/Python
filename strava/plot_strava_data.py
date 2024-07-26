#IMPORT MODULES
import numpy as np
import matplotlib.pyplot as plt

##Function to grab HH:MM:SS from <time>
def extract_time(line):
    #print(line)
    hour = float(line[17:19])
    #print('Hour = ',hour)
    minute = float(line[20:22])
    #print('Minute = ',minute)
    second = float(line[23:25])
    #print('Second = ',second)
    t = hour + minute/60.0 + second/3600.0
    return t

def extract_latlon(line):
    #print(line)
    row = line.split('"')
    #print(row)
    lt = float(row[1])
    ln = float(row[3])
    return lt,ln

def extract_ele(line):
    el = "".join(c for c in line if not c.isalpha())
    el = el.replace("<>","")
    el = el.replace("</>","")
    el = float(el)
    return el

def getlines(fullpath):
    length = 0
    file = open(fullpath)
    for line in file:
        length+=1
    file.close()
    print(fullpath,'LINES = ',length)
    return length

#READ IN STRAVA DATA
lat = []
lon = []
ele = []
time = []
filename = 'Elbert.gpx'
l = getlines(filename)
fid = open(filename)
ctr = 0
dp = 10.0
p = 0.0
for line in fid:
    #Notify user of progress
    if 100*(ctr/l) >= p:
        print('Percentage Complete = ',p)
        p+=dp
    #Make sure the line is over 4 characters
    if len(line) > 4:
        #remove all the spaces
        line = line.replace(" ","")
        #Search for time
        if line[0:6] == "<time>":
            ##Grab just the hour, minute and seconds
            t = extract_time(line)
            time.append(t)
        #Search for lat and lon
        if line[0:9] == "<trkptlat":
            lt,ln = extract_latlon(line)
            lat.append(lt)
            lon.append(ln)
        #Search for Elevation
        if line[0:5] == "<ele>":
            el = extract_ele(line)
            ele.append(el)
    #Break for debugging
    ctr+=1
    #if ctr == 200:
    #    break
print('Percentage Complete = ',100.0)

#Time has an extra timestamp
time = time[1:]
#Convert to numpy arrays
lat = np.array(lat)
lon = np.array(lon)
ele = np.array(ele)
time = np.array(time)-6
#Convert elevation to feet
ele = ele*3.28

##First Superimpose the google maps screenshot
im = plt.imread('Satellite.PNG')
# Display the image
implot = plt.imshow(im)
##CALIBRATION
image_start_pt = [633,76]
shape = np.shape(im)
image_size = [shape[0],shape[1]]
elbert_peak = [39.11799211481981, -106.4452547909551]
trail_head = [39.15184021965455, -106.41243251916767]
upper_left_corner = [39.15515323428226, -106.45612498908672]
lower_right_corner = [39.113795823152095, -106.39893201664289]
dlat = upper_left_corner[0] - lower_right_corner[0]
dlon = upper_left_corner[1] - lower_right_corner[1]
scalex = -image_size[0]/dlon
scaley = -image_size[1]/dlat*0.9
##Super impose the data
#fig = plt.figure()
#plti = fig.add_subplot(1,1,1)
scaled_lon = scalex*(lon-lon[0])+image_start_pt[0]
scaled_lat = scaley*(lat-lat[0])+image_start_pt[1]
scaled_elbertx = scalex*(elbert_peak[1]-lon[0])+image_start_pt[0]
scaled_elberty = scaley*(elbert_peak[0]-lat[0])+image_start_pt[1]
plt.plot(scaled_lon,scaled_lat,'b-',label='Route')
plt.grid()
plt.xlabel('Longitude (deg)')
plt.ylabel('Latitude (deg)')
plt.plot(scaled_lon[0],scaled_lat[0],'gx',label='Start Point')
plt.plot(scaled_lon[-1],scaled_lat[-1],'rx',label='End Point')
plt.plot(scaled_elbertx,scaled_elberty,'ms',label='Elbert')
#plti.get_yaxis().get_major_formatter().set_useOffset(False)
#plt.gcf().subplots_adjust(left=0.18)
plt.legend()

##plot RAW Lat vs Lon
fig = plt.figure()
plti = fig.add_subplot(1,1,1)
plti.plot(lon,lat,'b-',label='Route')
plti.grid()
plti.set_xlabel('Longitude (deg)')
plti.set_ylabel('Latitude (deg)')
plti.plot(lon[0],lat[0],'gx',label='Start Point')
plti.plot(lon[-1],lat[-1],'rx',label='End Point')
plti.plot(elbert_peak[1],elbert_peak[0],'ms',label='Elbert')
plti.plot(trail_head[1],trail_head[0],'y^',label='Trailhead')
plti.get_yaxis().get_major_formatter().set_useOffset(False)
plti.get_xaxis().get_major_formatter().set_useOffset(False)
plt.gcf().subplots_adjust(left=0.18)
plt.legend()

##Plot Lat Lon and Altitude
ax = plt.figure().add_subplot(projection='3d')
ax.plot(lon,lat,ele,'b-',label='Route')
plt.grid()
ax.set_xlabel('Longitude (deg)')
ax.set_ylabel('Latitude (deg)')
ax.set_zlabel('Altitude (ft)')
ax.plot(lon[0],lat[0],ele[0],'gx',label='Start Point')
ax.plot(lon[-1],lat[-1],ele[-1],'rx',label='End Point')
ax.plot(elbert_peak[1],elbert_peak[0],14439,'ms',label='Elbert')
ax.plot(trail_head[1],trail_head[0],10100,'y^',label='Trailhead')
plt.legend()

##Plot Elevation vs time
plt.figure()
plt.plot(time,ele)
plt.xlabel('Time (hrs)')
plt.ylabel('Elevation (ft)')
plt.grid()

##Elevation gain / min
plt.figure()
ele_gain = ((ele[1:]-ele[0:-1])/(time[1:]-time[0:-1])) / 60.0
ele_gain[ele_gain > 150] = 0
##Ele peaks
ele_gain_peaks = 0*ele_gain
ele_gain_peaks[0] = ele_gain[0]
for i in range(1,len(ele_gain)):
    if abs(ele_gain[i]) > 0:
        ele_gain_peaks[i] = ele_gain[i]
    else:
        ele_gain_peaks[i] = ele_gain_peaks[i-1]
##Filter
ele_gain_filter = 0*ele_gain
ele_gain_filter[0] = ele_gain_peaks[0]
s = 0.9
for i in range(0,len(ele_gain_peaks)-1):
    ele_gain_filter[i+1] = ele_gain_filter[i]*s + (1-s)*ele_gain_peaks[i]
#plt.plot(time[0:-1],ele_gain)
#plt.plot(time[0:-1],ele_gain_peaks)
plt.plot(time[0:-1],ele_gain_filter)
plt.xlabel('Time (hrs)')
plt.ylabel('Elevation gain / min')
plt.grid()

plt.show()