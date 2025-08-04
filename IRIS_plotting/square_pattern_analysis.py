#!/usr/bin/python

import sys
import os
import mio as MI
import numpy as np
import getpass
#Import mesonet module
sys.path.append('Mesonet')
import mesonet as MES
#Import pitot module
sys.path.append('FASTPitot/')
import pitot as FP
#Import imet module 
sys.path.append('iMet/')
import iMet as MET
#Import Quad module
#sys.path.append('Quad/')
import quad as Q #This has moved to BlackBox
#Import Anemometer module
sys.path.append('Anemometer/')
import anemometer as ANEM
#Import extra stuff
import gps as GPS
import mymath as M
import math
from pdf import PDF
import plotting as myplot
import matplotlib.pyplot as plt
import sixdof as SDOF

###Cost Function
def J(vtilde,v0,psi):
    J = 0.0
    for x in range(0,4):
        J += (vtilde[x]-pitot(v0,psi,x))**2
    return J
    
###Empirical Formula for Pitot probe
def pitot(v0,psi,i):
    psi_i = psi - (i)*np.pi/2 #Remember that python starts at 0 
    #if psi in between 135 and 225 vhat = 0 else use the formula below
    coeff = np.asarray([0.20343723,0.71429915,0.28590535,-0.24011622])
    c0 = 0.0530172884654
    ##Old data
    #coeff = np.asarray([0.14666216,0.66244758,0.23224845,-0.22226221])
    #c0 = -0.025
    ##Use empirical formula
    vhat = c0
    L = 2.0*np.pi
    N = len(coeff)
    for n in range(N):
        wn = 2.0*np.pi*(n+1)/L
        vhat += coeff[n]*np.cos(wn*psi_i)
    return vhat*v0
    
def Get_Pitot(v,psi):
    vout = []
    for x in range(0,4):
        vout.append(pitot(v0,psi,x))
    return(np.asarray(vout))

#Grab the pitot data
pFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/Quad_Square_Pattern/FP4V.TXT'
numPitots = 4
sigma_pitot = 0.03
#wc = 100.0 #this is set in pitot.py 
#truncation_bits = 1.5 #this is set in pitot.py
CAL_TIMES_i = [5,20]

# pFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/04_13_2017/FP4V/FP4V.TXT'
# numPitots = 4
# sigma_pitot = 1.0
# #wc = 100.0 #this is set in pitot.py 
# #truncation_bits = 1.5 #this is set in pitot.py
# CAL_TIMES_i = [25,35]

data_pitot = FP.get_pitot_data(pFile,numPitots,sigma_pitot,CAL_TIMES_i)

#Grab the quad data
qFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/Quad_Square_Pattern/ALLFILES.log'
#qFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/04_13_2017/FP4V/ALLFILES.log'
quad_data = Q.get_quad_data(qFile)

#Grab the mesonet data
mesFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/Quad_Square_Pattern/mobileusaw_2018-01-16_2018-01-16.csv'
#mesFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/04_13_2017/FP4V/mobileusaw_2017-04-13_2017-04-13.csv'
data_mes = MES.get_mesonet_data(mesFile)
time_mesonet = data_mes[0]
wind2 = data_mes[4]
wind10 = data_mes[5]
winddir2 = data_mes[6]
winddir10 = data_mes[7]

#Grab the Anemometer Data
anemometerFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/Quad_Square_Pattern/ANEM.TXT'
#anemometerFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/04_13_2017/FP4V/ANEM.TXT'
sigma_anemometer = 1.0
data_anem = ANEM.get_anemometer_data(anemometerFile,sigma_anemometer)
data_anem_gps = data_anem[0]
data_anem_wind = data_anem[1]
time_anemometer = data_anem_gps[2]
wind_anemometer = data_anem_wind[3]*1.65
anemometer_OneMin = M.averages(time_anemometer,wind_anemometer,1)

#Line Everything Up - Use Latitude and Longitude
gpsRead_all = quad_data[1]
IMURead = quad_data[3]
ATTRead = quad_data[4]
time_quad = gpsRead_all.time_quad
latitude_quad = gpsRead_all.latitude
longitude_quad = gpsRead_all.longitude

data_pitot_gps = data_pitot[0]
data_pitot_pitot = data_pitot[1]
time_pitot_gps = data_pitot_gps[2]+10.0/(3600.0) + (0.2215 - 0.22) #Off by 15.4 seconds
pitot_time_sec = data_pitot_pitot[0]
latitude_pitot = data_pitot_gps[0]
longitude_pitot = data_pitot_gps[1]

##Phi theta and Psi
################Need to Filter phi,theta, psi and p,q,r##################

ATTRead.ROLL_FILTER = np.copy(ATTRead.ROLL)
ATTRead.PITCH_FILTER = np.copy(ATTRead.PITCH)
ATTRead.YAW_FILTER = np.copy(ATTRead.YAW)
IMURead.GyrX_FILTER = np.copy(IMURead.GyrX)
IMURead.GyrY_FILTER = np.copy(IMURead.GyrY)
IMURead.GyrZ_FILTER = np.copy(IMURead.GyrZ)

s=0.0 ##This is a function of the update rate so we need different values for each one
#of these
for j in range(1,len(ATTRead.ROLL)):
    ATTRead.ROLL_FILTER[j] = ((s*ATTRead.ROLL_FILTER[j-1])+((1-s)*ATTRead.ROLL[j]))
print 'Filtered Roll'
for j in range(0,len(ATTRead.PITCH)):
    ATTRead.PITCH_FILTER[j] = ((s*ATTRead.PITCH_FILTER[j-1])+((1-s)*ATTRead.PITCH[j]))
print 'Filtered Pitch'
for j in range(0,len(ATTRead.YAW)):
    ATTRead.YAW_FILTER[j] = ((s*ATTRead.YAW_FILTER[j-1])+((1-s)*ATTRead.YAW[j]))
print 'Filtered Yaw'
s = 0.0 #Again different timing
for j in range(0,len(IMURead.GyrX)):
    IMURead.GyrX_FILTER[j] = ((s*IMURead.GyrX_FILTER[j-1])+((1-s)*IMURead.GyrX[j]))
print 'Filtered Gyrx'
for j in range(0,len(IMURead.GyrY)):
    IMURead.GyrY_FILTER[j] = ((s*IMURead.GyrY_FILTER[j-1])+((1-s)*IMURead.GyrY[j]))
print 'Filtered Gyry'
for j in range(0,len(IMURead.GyrZ)):
    IMURead.GyrZ_FILTER[j] = ((s*IMURead.GyrZ_FILTER[j-1])+((1-s)*IMURead.GyrZ[j]))
print 'Filtered Gyrz'

#######################################################################

#and then Interpolate the imu stream to gps stream
roll_interp = np.interp(gpsRead_all.timeSec,ATTRead.timeMS_ATT,ATTRead.ROLL_FILTER)
pitch_interp = np.interp(gpsRead_all.timeSec,ATTRead.timeMS_ATT,ATTRead.PITCH_FILTER)
yaw_interp = np.interp(gpsRead_all.timeSec,ATTRead.timeMS_ATT,ATTRead.YAW_FILTER)
gyrx_interp = np.interp(gpsRead_all.timeSec,IMURead.timeMS_IMU,IMURead.GyrX_FILTER)
gyry_interp = np.interp(gpsRead_all.timeSec,IMURead.timeMS_IMU,IMURead.GyrY_FILTER)
gyrz_interp = np.interp(gpsRead_all.timeSec,IMURead.timeMS_IMU,IMURead.GyrZ_FILTER)

print 'Interpolated roll, pitch, yaw, gyrxyz'

###################################################################

#Need Xdot,Ydot,Zdot
z_quad_deriv_not_interp = gpsRead_all.CLIMB_RATE
time_z_quad = np.asarray(gpsRead_all.timeMS_CTUN)-gpsRead_all.timeMS_CTUN[0]
z_quad_deriv = np.interp(gpsRead_all.timeSec,gpsRead_all.timeMS_CTUN,gpsRead_all.CLIMB_RATE)
#Need to interpolate z_quad

#To Get xdot and ydot I want to plot X and Y from GPS
origin = np.asarray([gpsRead_all.latitude[0],gpsRead_all.longitude[1]])
lat_lon = [gpsRead_all.latitude,gpsRead_all.longitude]
xyquad = GPS.convertLATLON(lat_lon,origin)
x_quad = xyquad[0]
y_quad = xyquad[1]

## So the derivative from x and y are horrible
# lat_lon_pitot = [latitude_pitot,longitude_pitot] 
# xypitot = GPS.convertLATLON(lat_lon_pitot,origin)
# x_pitot = xypitot[0]
# y_pitot = xypitot[1]

print 'Converted LAT LON to X,Y'

##################RUN X AND Y THROUGH A DERIVATIVE FILTER##########
#Is this np.gradient method accruate enough for this application? Hmmm. I guess we'll just have to plot it and see
#I didn't like np.gradient so I wrote my own
x_quad_deriv = np.copy(x_quad)
y_quad_deriv = np.copy(y_quad)
# x_pitot_deriv = np.copy(x_pitot)
# y_pitot_deriv = np.copy(y_pitot)

for j in range(1,len(x_quad)):
    x_quad_deriv[j] = (1.0/3600.0)*(x_quad[j]-x_quad[j-1])/(time_quad[j]-time_quad[j-1]) 
    y_quad_deriv[j] = (1.0/3600.0)*(y_quad[j]-y_quad[j-1])/(time_quad[j]-time_quad[j-1])
    # x_pitot_deriv[j] = (1.0/3600.0)*(x_pitot[j]-x_pitot[j-1])/(time_pitot_gps[j]-time_pitot_gps[j-1]) 
    # y_pitot_deriv[j] = (1.0/3600.0)*(y_pitot[j]-y_pitot[j-1])/(time_pitot_gps[j]-time_pitot_gps[j-1]) 

print 'Computed Derivative of X and Y'

##################MIGHT NEED FILTER FOR X AND Y###################

x_quad_deriv_filter = np.copy(x_quad_deriv)
y_quad_deriv_filter = np.copy(y_quad_deriv)
z_quad_deriv_filter = np.copy(z_quad_deriv)
# x_pitot_deriv_filter = np.copy(x_pitot_deriv)
# y_pitot_deriv_filter = np.copy(y_pitot_deriv)

s = 0.0 #I don't think we should filter these at all
for j in range(1,len(x_quad_deriv)):
    x_quad_deriv_filter[j] = ((s*x_quad_deriv_filter[j-1])+((1-s)*x_quad_deriv[j]))
for j in range(0,len(y_quad_deriv)):
    y_quad_deriv_filter[j] = ((s*y_quad_deriv_filter[j-1])+((1-s)*y_quad_deriv[j]))
for j in range(0,len(z_quad_deriv)):
    z_quad_deriv_filter[j] = ((s*z_quad_deriv_filter[j-1])+((1-s)*z_quad_deriv[j]))
# s = 0.0
# for j in range(0,len(x_pitot_deriv)):
#     x_pitot_deriv_filter[j] = ((s*x_pitot_deriv_filter[j-1])+((1-s)*x_pitot_deriv[j]))
# for j in range(0,len( y_pitot_deriv)):
#     y_pitot_deriv_filter[j] = ((s* y_pitot_deriv_filter[j-1])+((1-s)* y_pitot_deriv[j]))

print 'Used a Derivative Filter on X and Y deriv'
    
##################################################################

#Summary
#we have p,q,r, phi theta, psi ,xdot ,ydot and zdot of the quad all
#in the same data stream

##################Take the Pitot Raw Signal#################
###################Convert to V and PSI using J(v,psi)######

#Instead let's run this ahead of time and then import the data from a text file
data_from_algorithm = MI.dlmread('Compiled_Data/Lisa_Final_Thesis_Experiments/Quad_Square_Pattern/Algorithm_Output_N100.txt'," ")
#data_from_algorithm = MI.dlmread('Compiled_Data/Lisa_Final_Thesis_Experiments/04_13_2017/Algorithm_Output_FP4V_NoFilter.txt'," ")
#data_from_algorithm = MI.dlmread('Compiled_Data/Lisa_Final_Thesis_Experiments/04_13_2017/Algorithm_Output_FP4V_NoFilter_N100.txt'," ")
alg_v = data_from_algorithm[:,0]
alg_psi = data_from_algorithm[:,1]

###FILTER ALG_V AND ALG_PSI
alg_v_filter = np.copy(alg_v)
alg_psi_filter = np.copy(alg_psi)
sigma_alg = 1-0.03
for j in range(1,len(alg_v) ):
    alg_v_filter[j] = sigma_alg*alg_v_filter[j-1] + (1-sigma_alg)*alg_v[j]
    alg_psi_filter[j] = sigma_alg*alg_psi_filter[j-1] + (1-sigma_alg)*alg_psi[j]

VX = alg_v_filter*np.cos(alg_psi_filter*np.pi/180.0)
VY = alg_v_filter*np.sin(alg_psi_filter*np.pi/180.0)

#VX = data_from_algorithm[:,2]
#VY = data_from_algorithm[:,3]

pitot_signal_1 = data_pitot[1][1][0]
pitot_signal_2 = data_pitot[1][1][1]
pitot_signal_3 = data_pitot[1][1][2]
pitot_signal_4 = data_pitot[1][1][3]

##################INTERPOLATE ONE MORE TIME#################

#I think the pitot data stream is larger than the gps
#quad data stream so we need to interpolate the pitot data
#stream to the quad data stream and plot it to make sure it
#still matches
#for example interpolate the pitot longitude and it should still
#look right

VX_interp = np.interp(time_quad,time_pitot_gps,VX)
VY_interp = np.interp(time_quad,time_pitot_gps,VY)
VZ_interp = 0*VX_interp

#########USE THE KINEMATIC RELATIONSHIP TO GET VATM##########

rx = 0
ry = 0
rz = (-5.0/12.0)/3.28 #5 inches above platform

vatmx = []
vatmy = []
vatmz = []

print 'Kinematic Relationship'

for i in range( len(VX_interp) ):
    p = gyrx_interp[i]
    q = gyry_interp[i]
    r = gyrz_interp[i]

    #Angular Rate Substraction
    vx_angular = VX_interp[i] - (-r*ry + q*rz)
    vy_angular = VY_interp[i] - (r*rx  - p*rz)
    vz_angular = VZ_interp[i] - (-q*rx + p*ry)

    #Rotate to Body Frame
    phi = roll_interp[i]*np.pi/180.0
    theta = pitch_interp[i]*np.pi/180.0
    psi = yaw_interp[i]*np.pi/180.0
    R = SDOF.R123(phi,theta,psi)
    #%compute R such that v(inertial) = R v(body)
    vbody = np.asarray([vx_angular,vy_angular,vz_angular])
    vinertial = np.matmul(R,vbody)

    #Substract the xdot, ydot, zdot
    vatmx.append(vinertial[0]-x_quad_deriv[i])
    vatmy.append(vinertial[1]-y_quad_deriv[i])
    vatmz.append(vinertial[2]-z_quad_deriv[i])

###############MAYBE FILTER#################################

vatmx = np.asarray(vatmx)
vatmy = np.asarray(vatmy)
vatmz = np.asarray(vatmz)

################ONE MINUTE AVERAGES########################

#Let's also get scalar windspeed and direction
vscalar = np.sqrt(vatmx**2 + vatmy**2 + vatmz**2)
vdirection = -np.arctan(vatmy/vatmx)*180.0/np.pi

scalar_oneminute = M.averages(time_quad,vscalar,1)
dir_oneminute = M.averages(time_quad,vdirection,1)

############################################################

##############PLOT EVERYTHING

print 'Start plotting'

pp = PDF(0,plt)

FONTSIZE = 12
SETXLIM = 1
if SETXLIM:
    #For April 13th
    x0 = 14.0 + 6.0/60.0
    xf = 14.0 + 22.0/60.0
    #For square pattern
    x0 = 16.10
    xf = 16.45

####LATITUDE AND LONGITUDE
plti = myplot.plottool(FONTSIZE,'Time (hr)','Latitude (deg)','Latitude vs Time')
plti.plot(time_pitot_gps,latitude_pitot,label='Pitot')
plti.plot(time_quad,latitude_quad,label='Quad')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Longitude (deg)','Longitude vs Time')
plti.plot(time_pitot_gps,longitude_pitot,label='Pitot')
plti.plot(time_quad,longitude_quad,label='Quad')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Latitude (deg)','Longitude (deg)','Latitude vs. Longitude')
# plti.plot(latitude_pitot,longitude_pitot,label='Pitot')
plti.plot(latitude_quad,longitude_quad)
plti.legend()
pp.savefig()

print 'plot...'

###Plot All Data Streams
##Turns out IMU and GPS are logged at different rates as well so need to line those up
plti = myplot.plottool(FONTSIZE,'Num data points','Time of Sensor (sec)','Timers')
plti.plot(gpsRead_all.timeSec,label='GPS')
plti.plot(IMURead.timeMS_IMU,label='IMU')
plti.plot(pitot_time_sec,label='Pitot')
plti.legend()
pp.savefig()

print 'plot...'

###X AND Y
plti = myplot.plottool(FONTSIZE,'Time (hr)','X (m)','X vs Time')
# plti.plot(time_pitot_gps,x_pitot,label='Pitot')
plti.plot(time_quad,x_quad,label='Quad')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Y (m)','Y vs Time')
# plti.plot(time_pitot_gps,y_pitot,label='Pitot')
plti.plot(time_quad,y_quad,label='Quad')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'X (m)','Y (m)','X vs Y')
# plti.plot(x_pitot,y_pitot,label='Pitot')
plti.plot(x_quad,y_quad,label='Quad')
plti.legend()
pp.savefig()

print 'plot...'

#X and Y derivative
# plti = myplot.plottool(FONTSIZE,'Time (hr)','X dot (m/s)','Xdot vs Time')
# plti.plot(time_pitot_gps,x_pitot_deriv,label='Pitot')
# plti.plot(time_pitot_gps,x_pitot_deriv_filter,label='Pitot Filtered')
# plti.legend()
# pp.savefig()

# print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','X dot (m/s)','Xdot vs Time')
plti.plot(time_quad,x_quad_deriv,label='Quad')
plti.plot(time_quad,x_quad_deriv_filter,label='Quad Filtered')
if SETXLIM:
    #plti.set_xlim([x0,xf])
    myplot.xlim_auto(x0,xf,time_quad,x_quad_deriv)
plti.legend()
pp.savefig()

print 'plot...'

# plti = myplot.plottool(FONTSIZE,'Time (hr)','Y dot (m/s)','Ydot vs Time')
# plti.plot(time_pitot_gps,y_pitot_deriv,label='Pitot')
# plti.plot(time_pitot_gps,y_pitot_deriv_filter,label='Pitot Filtered')
# plti.legend()
# pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','Y dot (m/s)','Ydot vs Time')
plti.plot(time_quad,y_quad_deriv,label='Quad')
plti.plot(time_quad,y_quad_deriv_filter,label='Quad Filtered')
if SETXLIM:
    myplot.xlim_auto(x0,xf,time_quad,y_quad_deriv)
    #plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','abs(XY) dot (m/s)','X/Ydot vs Time')
plti.plot(time_quad,np.abs(y_quad_deriv_filter))
plti.plot(time_quad,np.abs(x_quad_deriv_filter))
if SETXLIM:
    #plti.set_xlim([x0,xf])
    myplot.xlim_auto(x0,xf,time_quad,np.abs(y_quad_deriv_filter))
plti.legend()
pp.savefig()

print 'plot...'

# plti = myplot.plottool(FONTSIZE,'Time (sec)','Z dot (m/s)','Zdot vs Time')
# plti.plot(time_z_quad,z_quad_deriv_not_interp,label='Quad')
# plti.plot(time_z_quad,z_quad_deriv_filter,label='Quad Filtered')
# plti.legend()
# pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Z dot (m/s)','Zdot vs Time')
plti.plot(time_quad,z_quad_deriv,label='Quad')
plti.plot(time_quad,z_quad_deriv_filter,label='Quad Filtered')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

###ROLL AND PITCH OF QUAD
plti = myplot.plottool(FONTSIZE,'Time (ms)','Angle (deg)','Roll vs Time')
plti.plot(ATTRead.timeMS_ATT,ATTRead.ROLL,label='Roll')
plti.plot(ATTRead.timeMS_ATT,ATTRead.ROLL_FILTER,label='Roll Filtered')
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (ms)','Angle (deg)','Pitch vs Time')
plti.plot(ATTRead.timeMS_ATT,ATTRead.PITCH,label='Pitch')
plti.plot(ATTRead.timeMS_ATT,ATTRead.PITCH_FILTER,label='Pitch Filtered')
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Angle (deg)','Roll and Pitch vs Time')
plti.plot(time_quad,roll_interp,label='Roll')
plti.plot(time_quad,pitch_interp,label='Pitch')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

###Yaw of Quad
plti = myplot.plottool(FONTSIZE,'Time (sec)','Angle (deg)','Yaw vs Time')
plti.plot(ATTRead.timeMS_ATT,ATTRead.YAW,label='Yaw')
plti.plot(ATTRead.timeMS_ATT,ATTRead.YAW_FILTER,label='Yaw Filtered')
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Angle (deg)','Yaw vs Time')
plti.plot(time_quad,(yaw_interp))
if SETXLIM:
    plti.set_xlim([x0,xf])
pp.savefig()

print 'plot...'

###Gyro Data
plti = myplot.plottool(FONTSIZE,'Time (ms)','Angular Rate (rad/s)','Angular Rate Data')
plti.plot(IMURead.timeMS_IMU,IMURead.GyrX,label='GyroX')
plti.plot(IMURead.timeMS_IMU,IMURead.GyrX_FILTER,label='GyroX Filtered')
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (ms)','Angular Rate (rad/s)','Angular Rate Data')
plti.plot(IMURead.timeMS_IMU,IMURead.GyrY,label='GyroY')
plti.plot(IMURead.timeMS_IMU,IMURead.GyrY_FILTER,label='GyroY Filtered')
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (ms)','Angular Rate (rad/s)','Angular Rate Data')
plti.plot(IMURead.timeMS_IMU,IMURead.GyrZ,label='GyroZ')
plti.plot(IMURead.timeMS_IMU,IMURead.GyrZ_FILTER,label='GyroZ Filtered')
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Anglular Rate (rad/s)','Angular Rate Data Interpolated')
plti.plot(time_quad,gyrx_interp,label='X')
plti.plot(time_quad,gyry_interp,label='Y')
plti.plot(time_quad,gyrz_interp,label='Z')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

###Data Points
plti = myplot.plottool(FONTSIZE,'Time (hr)','Raw Measured Velocity (m/s)','Measured Velocity')
plti.plot(time_pitot_gps,pitot_signal_1, label='East Sensor')
plti.plot(time_pitot_gps,pitot_signal_2, label='South Sensor')
plti.plot(time_pitot_gps,pitot_signal_3, label='West Sensor')
plti.plot(time_pitot_gps,pitot_signal_4, label='North Sensor')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

##Plot scalar speed and direction from Algorithm
plti = myplot.plottool(FONTSIZE,'Time (hr)','Scalar Wind Speed (m/s)','Algorithm')
plti.plot(time_pitot_gps,alg_v)
plti.plot(time_pitot_gps,alg_v_filter,label='filtered')
if SETXLIM:
    plti.set_xlim([x0,xf])
# plti.plot(time_quad,np.sqrt(x_quad_deriv**2 + y_quad_deriv**2))
# plti.plot(time_pitot_gps,pitot_signal_1, label='East Sensor')
# plti.plot(time_pitot_gps,pitot_signal_2, label='South Sensor')
# plti.plot(time_pitot_gps,pitot_signal_3, label='West Sensor')
# plti.plot(time_pitot_gps,pitot_signal_4, label='North Sensor')
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Direction (deg)','Algorithm')
plti.plot(time_pitot_gps,alg_psi)
plti.plot(time_pitot_gps,alg_psi_filter,label='filter')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

###Plot VX, VY since VZ is zero
plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Speed (m/s)','Algorithm')
plti.plot(time_pitot_gps,VX, label='VX')
plti.plot(time_quad,VX_interp, label='VX interp')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Speed (m/s)','Algorithm')
plti.plot(time_pitot_gps,VY, label='VY')
plti.plot(time_quad,VY_interp, label='VY interp')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

#Kinematic Relationships
plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Speed (m/s)','Output from Kinematic')
plti.plot(time_quad,vatmx, label='VX')
if SETXLIM:
    #plti.set_xlim([x0,xf])
    myplot.xlim_auto(x0,xf,time_quad,vatmx)
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Speed (m/s)','Output from Kinematic')
plti.plot(time_quad,vatmy, label='VY')
if SETXLIM:
    #plti.set_xlim([x0,xf])
    myplot.xlim_auto(x0,xf,time_quad,vatmy)
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Speed (m/s)','Output from Kinematic')
plti.plot(time_quad,vatmz, label='VZ')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

###Final Plots
plti = myplot.plottool(10,'Time (hr)','Wind Speed (m/s)','Scalar Wind Speed Comparison')
#plti.plot(time_quad,vscalar, label='FP4V')
plti.plot(scalar_oneminute[0],scalar_oneminute[1], label='FP4V One Minute Average')
plti.plot(time_mesonet,wind2,label='Mesonet Tower 2m')
plti.plot(time_mesonet,wind10,label='Mesonet Tower 10m')
#plti.plot(time_anemometer,wind_anemometer,label='Anemometer')
plti.plot(anemometer_OneMin[0],anemometer_OneMin[1],label='Anemometer One Minute Average')
if SETXLIM:
    plti.set_xlim([x0,xf])
    #myplot.xlim_auto(x0,xf,time_mesonet,wind10)
plti.legend(loc='best')
#plti.legend(bbox_to_anchor=(1.05, 1), loc=2)
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Direction (deg)','Direction of Wind')
#plti.plot(time_quad,vdirection, label='FP4V')
plti.plot(dir_oneminute[0],dir_oneminute[1], label='FP4V One Minute Average')
plti.plot(time_mesonet,M.unwrap_simple(winddir2),label='Mesonet Tower 2m')
plti.plot(time_mesonet,M.unwrap_simple(winddir10),label='Mesonet Tower 10m')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.set_ylim([-180,180])
plti.legend(loc='best')
pp.savefig()

pp.close()




