import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

##Open file
fid = open('Elbert.gpx')

##Create empty arrays
latitude_vec = []
longitude_vec = []
time_vec = []
ele_vec = []

##Loop through file
for line in fid:
    ##make sure the line we're looking for is greater than 0
    if len(line) > 3:
        no_space = line.replace(" ","")
        no_newline = no_space.replace("\n","")
        if "<trkpt" in no_newline:
            #print(no_newline)
            row = no_newline.split('"')
            #print(row)
            lat = float(row[1])
            lon = float(row[3])
            latitude_vec.append(lat)
            longitude_vec.append(lon)
        if "<ele>" in no_newline:
            no_left = no_newline.replace("<","")
            no_right = no_left.replace(">","")
            no_slash = no_right.replace("/","")
            row = no_slash.split("e")
            #print(row)
            ele = float(row[2])
            ele_vec.append(ele)
        if "<time>" in no_newline:
            no_slash = no_newline.replace("/","")
            row = no_slash.split("<time>")
            #print(row)
            all_time = row[1]
            time = all_time[11:19]
            #print(time)
            hms = time.split(":")
            hours = hms[0]
            minutes = hms[1]
            seconds = hms[2]
            hour = float(hours) + float(minutes)/60. + float(seconds)/3600.0
            time_vec.append(hour)
            

latitude_vec = np.array(latitude_vec)
longitude_vec = np.array(longitude_vec)
ele_vec = np.asarray(ele_vec)*3.28
time_vec = np.asarray(time_vec)
time_vec = time_vec[1:]

fig,ax = plt.subplots()
ax.plot(longitude_vec,latitude_vec)
ax.xaxis.get_major_formatter().set_useOffset(False)
ax.plot(longitude_vec[0],latitude_vec[0],'gs',markersize=20)
msg = 'Started at = ' + str(latitude_vec[0]) + ' ' + str(longitude_vec[0])
print(msg)
plt.title(msg)
plt.grid()

##3d plot (Strava makes you pay for this. And we're not doing that)
# Create the figure and 3D axes0
fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
# Create the plot plot
ax1.plot(longitude_vec,latitude_vec,ele_vec)
ax1.xaxis.get_major_formatter().set_useOffset(False)

fig2 = plt.figure()
plt.plot(time_vec,ele_vec)
plt.grid()

plt.show()
            