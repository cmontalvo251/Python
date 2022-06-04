#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from math import *
from matplotlib.backends.backend_pdf import PdfPages
import sys
import os

def convert_time(input,hms):
    hrs = np.float(input[0:2])
    min = np.float(input[3:5])
    sec = np.float(input[6:8])
    #print hrs,min,sec
    if hms == 0:
        output = hrs + min/60 + sec/3600
    elif hms == 1:
        output = hrs*60 + min + sec/60
    elif hms == 2:
        output = hrs*3600 + min*60 + sec
    #print output
    return output

file = open('Data_Jude_Breaux.csv')

lap_num_vec = []
time_hrs_vec = []
lap_time_min_vec = []
lap_time_hrs_vec = []
TOD_hrs_vec = []
dist_vec = []
speed_vec = []
offset = 0

for line in file:
    if line[0] != 'S':
        #print line
        row = line.split(',')

        #Lap Number
        lap_num = row[0]
        lap_num_vec.append(np.float(lap_num[4:]))

        #Current Time
        time = convert_time(row[1],0)
        time_hrs_vec.append(time)

        #Lap Time
        time = convert_time(row[2],1)
        lap_time_min_vec.append(time)
        time = convert_time(row[2],0)
        lap_time_hrs_vec.append(time)

        #Speed
        speed_vec.append(1.46/time)

        #Time of Day
        time = convert_time(row[3],0)
        if time < 9 and offset == 0:
            offset = 24
        TOD_hrs_vec.append(time+offset)

        #Distance 
        dist_vec.append(np.float(row[7]))

#print lap_num_vec
#print time_hrs_vec
#print lap_time_min_vec
#print TOD_hrs_vec
#print dist_vec

#PLOT DATA
os.system('rm plots.pdf')
pp = PdfPages('plots.pdf')

plt.figure()
plt.plot(time_hrs_vec,dist_vec,marker='s')
plt.xlabel('Time Since Start (Hrs)')
plt.ylabel('Distance (miles)')
plt.grid()
pp.savefig()

plt.figure()
plt.plot(time_hrs_vec,lap_num_vec,marker='s')
plt.xlabel('Time Since Start (Hrs)')
plt.ylabel('Lap Number')
plt.grid()
pp.savefig()

plt.figure()
plt.plot(time_hrs_vec,lap_time_min_vec,marker='s')
plt.xlabel('Time Since Start (Hrs)')
plt.ylabel('Lap Time (min)')
plt.grid()
pp.savefig()

plt.figure()
plt.plot(time_hrs_vec,lap_time_min_vec,marker='s')
plt.xlabel('Time Since Start (Hrs)')
plt.ylabel('Lap Time (min)')
plt.ylim((5,12))
plt.grid()
pp.savefig()

plt.figure()
plt.plot(TOD_hrs_vec,lap_time_min_vec,marker='s')
plt.xlabel('Time of Day (Hrs)')
plt.ylabel('Lap Time (min)')
plt.grid()
pp.savefig()

plt.figure()
plt.plot(TOD_hrs_vec,speed_vec,marker='s')
plt.xlabel('Time of Day (Hrs)')
plt.ylabel('Speed (m/s)')
plt.grid()
pp.savefig()

plt.figure()
plt.plot(TOD_hrs_vec,speed_vec,marker='s')
plt.xlabel('Time of Day (Hrs)')
plt.ylabel('Speed (m/s)')
plt.grid()
plt.ylim((7,14))
pp.savefig()

#CLOSE FILE
pp.close()

print 'Plots Saved'

#AND THEN USE EVINCE TO OPEN PDF if on linux
if sys.platform == 'linux2':
    os.system('evince plots.pdf &')
        
