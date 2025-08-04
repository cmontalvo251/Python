#!/usr/bin/python

from pdf import *
import plotting as P
import mio as I
import sys
from mymath import unwrap
import numpy as np
#import plot_HAT as S
sys.path.append('FASTPitot/')
import pitot as Pit
sys.path.append('Mesonet/')
import mesonet as M
sys.path.append('Anemometer/')
import anemometer as ANEM 
import gps as GPS

pp = PDF(0,plt) #0 = pdf and 1 = show them here

if len(sys.argv) > 1:
    root_dir = sys.argv[1]
else:
    root_dir = ''
print root_dir
hatFile = 'NOT FOUND'

#find the snese hat file
for root,dirs,files in os.walk(root_dir):
    for fname in files:
        path=os.path.join(root,fname)
        #Check for symbolic link
        if not os.path.islink(path):
            #Check for .log files
            filename, file_extension = os.path.splitext(path)

            #This checks for hat File
            if file_extension == '.txt':
                    
                if len(fname) > 2:
                        #Check if the first 3 characters are hat
                    print fname[0:2]
                    if fname[0:3] == 'PTH':
                        hatFile = path
print 'Using HATFile = ' + hatFile
#grab mesonetfile
mesonetFile = 'NOT FOUND'
for root,dirs,files in os.walk(root_dir):
    for fname in files:
        path=os.path.join(root,fname)
        #Check for symbolic link
        if not os.path.islink(path):
            #Check for .log files
            filename, file_extension = os.path.splitext(path)

            #This checks for Mesonet File
            if file_extension == '.csv':
                #This is either iMet or Mesonet
                if len(fname) > 10:
                    #Check if the first 10 characters are Mesonet
                    print fname[0:10]
                    if fname[0:10] == 'mobileusaw':
                        mesonetFile = path
anemFile = root_dir + '/ANEM0.TXT'
anemFile2 = root_dir + '/ANEM1.TXT'
pitotFile = root_dir + '/FP4V.TXT'
pitotFile2 = root_dir + '/FP4H.TXT'
sigma = 0.03
#grab every data ball known to man 
anem0Data = ANEM.get_anemometer_data(anemFile,sigma)
anem1Data = ANEM.get_anemometer_data(anemFile2,sigma)
pitot0Data = Pit.get_pitot_data(pitotFile,4,sigma,[-99,0])
pitot1Data = Pit.get_pitot_data(pitotFile2,4,sigma,[-99,0])
data_meso = M.get_mesonet_data(mesonetFile)
#datahat = S.get_HAT_data(hatFile)
#time_hat = np.array(datahat[0])
#pressure = datahat[1]
#temp4 = datahat[2]
#rh = datahat[3]
if data_meso != None:
    timetot_np = data_meso[0]
    press = data_meso[14]
    temp = data_meso[12]
    hum = data_meso[13]
timer_a = np.array(anem0Data[0])
temp0 = anem0Data[2][1]
temp1 = anem1Data[2][1]
temp2 = pitot1Data[2][1]
temp3 = pitot0Data[2][1]
time0 = GPS.HHMM_Format(anem1Data[0][2],1)
time1 = GPS.HHMM_Format(pitot0Data[0][2],1)
time2 = GPS.HHMM_Format(pitot1Data[0][2],1)
press0 = anem0Data[2][2]
press1 = anem1Data[2][2]
press2 = pitot0Data[2][2]
press3 = pitot1Data[2][2]
rh0 = anem0Data[2][3]
rh1 = anem1Data[2][3]
rh2 = pitot0Data[2][3]
rh3 = pitot1Data[2][3]
#the issue is that mesonet does not line up wth snese hat time (ain't that some shit)
#I need to loop through the gps time from the mesonet and check to see if it matches the gps time from 
#the arduino. if it does set it equal to the arduino timer

#nah, fuck that, Let's add the arduino gps time to the pi timer
gps_arduino = anem0Data[0][2]
#gps_pi = GPS.HHMM_Format((time_hat)/3600 + gps_arduino[0],1)
GPS_arduino = np.array(GPS.HHMM_Format(anem0Data[0][2],1))
##^^^Here's the issue. GPS.HHMM_Format returns two things - so this won't work.
print '!!!!!!!!!!!!!!!!!!!!'
print '!!!!!!!!!!!!!!!!!!!!'
print '!!!!!!!!!!!!!!!!!!!!'
np.set_printoptions(threshold=np.nan)
#print GPS_arduino[0] ##what's this? 
#print len(GPS_arduino[0])
print anem0Data[-1]
#GPS data is anem0Data[0]
print anem0Data[0][-1]
#tot_time_hr is [2]
print 'tot_time_hr length = ',len(anem0Data[0][2])
#PTH is anem0Data[2]
print anem0Data[2][-1]
#Temperature is [1]
print 'Temperature length = ',len(anem0Data[2][1])
#so temp0 = anem0Data[2][1] ok cool
#print temp0 ##I think this is temperature

##Alright so tot_time_hr and temp0 are the same lengths
##Ok co sollin is using the GPS.HHMM_Format function incorrectly
##This is how to properly do it
time_vec_HHMM,xticks = GPS.HHMM_Format(anem0Data[0][2],5.0)

#xticks = 120 -- Not sure why you have this here 
#fig = plt.figure() -- Plottool takes care of all of this
#plt.grid()
plti = P.plottool(12,'Time (sec)','Temperature (C)','Temperature vs. Time')
if anem0Data != None:
    #plti.plot(GPS_arduino[0],temp0,label='Anemometer 0')
    #You're not supposed to plot the output of GPS.HHMM
    #Plot the normal data
    plti.plot(anem0Data[0][2],anem0Data[2][1],label='Anemometer 0')
    ##Then do all this shit 
    plti.set_xlabel('Time (HH:MM)')
    plti.set_ylabel('Altitude (m)')
    plti.legend(loc='best')
    plti.set_xticks(xticks) 
    plti.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    #I'm going to throw a pp.savefig() and pp.close() so I can test
    pp.savefig()
    #pp.close()
    #sys.exit()
    print 'anem 0 plotted'
if anem1Data != None:
    plti.plot(time0,temp1,label='Anemometer 1')
if pitot0Data != None:
    plti.plot(time1,temp3,label='FP4V')
if pitot1Data != None:
    plti.plot(time2,temp2,label='FP4H')
if hatFile!= None:
    plti.plot(gps_pi,temp4,label = 'Sense HAT')
if mesonetFile!= None:
    if len(temp[0]) > 0:
        temp_height = temp[4]
        #fig = plt.figure()
        p = fig.add_subplot(1,1,1)
        for i in range(0,4):
            plt.plot(timetot_np,temp[i],label='Mesonet '+str(temp_height[i])+' m')
        
plt.xlim(gps_arduino[0],gps_arduino[-1])
    
plt.legend(bbox_to_anchor=(0.45, 0.57),bbox_transform=plt.gcf().transFigure)
pp.savefig()

fig0 = plt.figure()
plt.grid()
plti = P.plottool(12,'Time (sec)','Pressure (mb)','Pressure vs. Time')
if anem0Data != None:
    plti.plot(GPS_arduino,press0,label='Anemometer 0')
if anem1Data != None:
    plti.plot(time0,press1,label='Anemometer 1')
if pitot0Data != None:
    plti.plot(time1,press2,label='FP4V')
if pitot1Data != None:
    plti.plot(time2,press3,label='FP4H')
#if hatFile!= None:
    #plti.plot(gps_pi,pressure,label = 'Sense HAT')
if mesonetFile != None:
    if len(press[0]) > 0:
        #fig = plt.figure()
        p = fig.add_subplot(1,1,1)
        for i in range(0,2):
            #print press[i]
            plt.plot(timetot_np,press[i],label='Mesonet '+str(i))
        plt.xlabel('Time (hour)')
        plt.ylabel('Pressure (hPa)')
        #p.set_xticks(xticks) 
        #p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
        axes = plt.gca()
        axes.set_xlim([timetot_np[0],timetot_np[-1]])    
        plt.legend(loc='best')
        p.get_yaxis().get_major_formatter().set_useOffset(False)
        
plt.xlim(gps_arduino[0],gps_arduino[-1])
plt.legend(bbox_to_anchor=(0.05, 0.7, 0.65, 0.9), loc=3,ncol=2, mode="expand", borderaxespad=0.)
pp.savefig()

fig1 = plt.figure()
plt.grid()
plti = P.plottool(12,'Time (sec)','Humidity (%)','Humidity vs. Time') 
if anem0Data != None:
    plti.plot(GPS_arduino,rh0,label='Anemometer 0') 
if anem1Data != None:
    plti.plot(time0,rh1,label='Anemometer 1') 
if pitot0Data != None:
    plti.plot(time1,rh2,label='FP4V') 
if pitot1Data != None:
    plti.plot(time2,rh3,label='FP4H') 
#if hatFile!= None:
    #plti.plot(gps_pi,rh,label = 'Sense HAT')
if mesonetFile!= None:
    if len(hum[0]) > 0:
        hum_height = hum[2]
        #fig = plt.figure()
        p = fig.add_subplot(1,1,1)
        for i in range(0,len(hum_height)):
            plt.plot(timetot_np,hum[i],label='Mesonet '+str(hum_height[i])+' m')
        plt.xlabel('Time (hour)')
        plt.ylabel('Humidity (%)')
        #p.set_xticks(xticks) 
        #p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
        axes = plt.gca()
        axes.set_xlim([timetot_np[0],timetot_np[-1]])    
        plt.legend(loc='best')
        
plt.xlim(gps_arduino[0],gps_arduino[-1])
plt.legend(bbox_to_anchor=(0.05, 0.7, 0.8, 0.9), loc=3,ncol=2, mode="expand", borderaxespad=0.)
pp.savefig()

pp.close()
