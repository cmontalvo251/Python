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
sys.path.append('/home/files/Docs/GitLab_Repos/Research/FASTPilot/FASTWing/')
import fastwing as FW

#Grab the Apprentice Data
sigma_pitot_apprentice = 0.22
#wc = 100 #set in pitot.py
#truncation bits = 1.5
debugmode = 0
metafile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/Apprentice_Square_Pattern/Apprentice_META062.TXT'
fastwing_data = FW.get_fast_wing_data(metafile,0,sigma_pitot_apprentice,debugmode)

time_apprentice = fastwing_data.tot_time_np
latitude_apprentice = fastwing_data.GPS.latitude
longitude_apprentice = fastwing_data.GPS.longitude
pitot_speed = fastwing_data.pitot_speed
#pitot_speed_filtered = fastwing_data.pitot_speed_filtered

#Grab the Anemometer Data
anemometerFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/Apprentice_Square_Pattern/Anem0_GPSLO046.TXT'
sigma_anemometer = 1.0
data_anem = ANEM.get_anemometer_data(anemometerFile,sigma_anemometer)
data_anem_gps = data_anem[0]
data_anem_wind = data_anem[1]
time_anemometer = data_anem_gps[2]
wind_anemometer = data_anem_wind[3]
anemometer_OneMin = M.averages(time_anemometer,wind_anemometer,1)

#Get GPS Velocity

velocity_apprentice_gps = fastwing_data.GPS.speed_ms

##Let's Get Phi theta and psi now##################################

roll_apprentice = fastwing_data.IMU.roll_np
pitch_apprentice = fastwing_data.IMU.pitch_np
yaw_apprentice = fastwing_data.IMU.pitch_np
p_app = fastwing_data.IMU.p_np
q_app = fastwing_data.IMU.q_np
r_app = fastwing_data.IMU.r_np
#Note that there is also gps heading
heading_apprentice = M.unwrap_simple(fastwing_data.GPS.angle_np)
#There is also sensor fusion happening on the Arduino Mega
#heading_fusion_apprentice = fastwing_data.filtered_heading_np -- this one sucks. Gonna have to fuse myself
heading_fusion_apprentice = np.copy(yaw_apprentice)

for j in range ( len(heading_fusion_apprentice) ):
    #First things first. If the apprentice isn't moving you should just use the IMU
    if velocity_apprentice_gps[j] < 1:
        heading_fusion_apprentice[j] = yaw_apprentice[j]
    else:
        #Otherwise you need to do a blend between the IMU and GPS
        s = 0.2
        heading_fusion_apprentice[j] = s*yaw_apprentice[j] + heading_apprentice[j]
        

###################################################################

#Need Xdot,Ydot,Zdot
#To Get xdot and ydot I want to plot X and Y and Altitude from GPS
origin = np.asarray([latitude_apprentice[0],longitude_apprentice[1]])
lat_lon = [latitude_apprentice,longitude_apprentice]
xyapp = GPS.convertLATLON(lat_lon,origin)
x_apprentice = -xyapp[0]
y_apprentice = -xyapp[1]
z_apprentice = fastwing_data.GPS.altitude

print 'Converted LAT LON to X,Y'

##################RUN X,Y and Z THROUGH A DERIVATIVE FILTER##########

SAT = 3600*20.0 #based on GPS speed
x_array = M.Derivative(x_apprentice,time_apprentice,SAT)
x_apprentice_deriv = x_array[0]
y_array = M.Derivative(y_apprentice,time_apprentice,SAT)
y_apprentice_deriv = y_array[0]
z_array = M.Derivative(z_apprentice,time_apprentice,SAT)
z_apprentice_deriv = z_array[0]

FILTER = 'Complimentary'

if FILTER == 'LowPass':
    wc = 10000.0 #cutoff frequency. Will need to tune
    x_filter = M.LowPass(x_apprentice_deriv,time_apprentice,wc)
    x_apprentice_deriv_filter = x_filter[0]
    y_filter = M.LowPass(y_apprentice_deriv,time_apprentice,wc)
    y_apprentice_deriv_filter = y_filter[0]
    z_filter = M.LowPass(z_apprentice_deriv,time_apprentice,wc)
    z_apprentice_deriv_filter = z_filter[0]
elif FILTER == 'Complimentary':
    s = 0.03
    x_apprentice_deriv_filter = M.Complimentary(s,x_apprentice_deriv)*(0.1/s) #scaled to match GPS
    y_apprentice_deriv_filter = M.Complimentary(s,y_apprentice_deriv)*(0.1/s)
    z_apprentice_deriv_filter = M.Complimentary(s,z_apprentice_deriv)*(0.1/s)

x_apprentice_deriv_filter = x_apprentice_deriv_filter*(1.0/3600.0)
y_apprentice_deriv_filter = y_apprentice_deriv_filter*(1.0/3600.0)
z_apprentice_deriv_filter = z_apprentice_deriv_filter*(1.0/3600.0)
velocity_apprentice_deriv_filter = np.sqrt(x_apprentice_deriv_filter**2 + y_apprentice_deriv_filter**2 + z_apprentice_deriv_filter**2)

#Another option is to get the speed of the aircraft and assume the velocity in the body frame
#is VB/I = [u,0,0] and then rotate it to the inertial frame using the rotation of the aircraft.
#Let's try that.
#velocity_apprentice_gps = fastwing_data.GPS.speed_ms --moved to above to help with heading sensor fusion
x_apprentice_deriv_gps = np.copy ( velocity_apprentice_deriv_filter )
y_apprentice_deriv_gps = np.copy ( velocity_apprentice_deriv_filter )
z_apprentice_deriv_gps = np.copy ( velocity_apprentice_deriv_filter )

##Go ahead and fix Pitot data
pitot_speed_filtered = np.copy ( pitot_speed )
l = np.where(abs(velocity_apprentice_gps) < 1.0)[0]
pitot_speed_filtered[l] = 0.0
pitot_speed_filtered = M.Complimentary(sigma_pitot_apprentice,pitot_speed_filtered)

# Need to also get pitot data from FP4 sensor
pFile = 'Compiled_Data/Lisa_Final_Thesis_Experiments/Apprentice_Square_Pattern/FP4V_GPSLO103.TXT'
numPitots = 4
sigma_pitot = 0.22 #this turns everything off
#wc = 100.0 #this is set in pitot.py 
#truncation_bits = 1.5 #this is set in pitot.py
CAL_TIMES_i = [-99,0]
data_pitot = FP.get_pitot_data(pFile,numPitots,sigma_pitot,CAL_TIMES_i)
# And the data from running the FP4 data through the algorithm
data_from_algorithm = MI.dlmread('Compiled_Data/Lisa_Final_Thesis_Experiments/Apprentice_Square_Pattern/Algorithm_Output_N100.txt'," ")

data_pitot_gps = data_pitot[0]
time_pitot = data_pitot_gps[2] #No offset needed. Plots match up just fine.
latitude_pitot = data_pitot_gps[0]
longitude_pitot = data_pitot_gps[1]

alg_v = data_from_algorithm[:,0]
alg_psi = data_from_algorithm[:,1]

###FILTER ALG_V AND ALG_PSI
alg_v_filter = np.copy(alg_v)
alg_psi_filter = np.copy(alg_psi)
s = 1-0.22
for j in range(1,len(alg_v) ):
    alg_v_filter[j] = s*alg_v_filter[j-1] + (1-s)*alg_v[j]
    alg_psi_filter[j] = s*alg_psi_filter[j-1] + (1-s)*alg_psi[j]
    if time_pitot[j] > 21.426:
        alg_v_filter[j] = 0.0

VX = alg_v_filter*np.cos(alg_psi_filter*np.pi/180.0)
VY = alg_v_filter*np.sin(alg_psi_filter*np.pi/180.0)

pitot_signal_1 = data_pitot[1][1][0]
pitot_signal_2 = data_pitot[1][1][1]
pitot_signal_3 = data_pitot[1][1][2]
pitot_signal_4 = data_pitot[1][1][3]

##################INTERPOLATE ONE MORE TIME#################

#The apprentice is on longer so you need to interpolate everything to the FP4.
#Problem is the FP4 is so spare I'd rather try and see if we can interpolate to the
#apprentice

VX_interp = np.interp(time_apprentice,time_pitot,VX)
VY_interp = np.interp(time_apprentice,time_pitot,VY)
VZ_interp = 0*VX_interp

#########AND USE THE KINEMATIC RELATIONSHIP TO GET VATM##########

rx = (5.0/12.0)/3.28
ry = -(15.0/12.0)
rz = (-3.0/12.0)/3.28

rx4 = 0.0
ry4 = 0.0
rz4 = (-3.0/12.0)/3.28 + -(5.0/12.0)/3.28

vatmx = []
vatmy = []
vatmz = []

vatmx4 = []
vatmy4 = []
vatmz4 = []

print 'Kinematic Relationship'

for j in range ( len(velocity_apprentice_gps) ):
    #Rotate to Body Frame
    phi = roll_apprentice[j]*np.pi/180.0 
    theta = pitch_apprentice[j]*np.pi/180.0
    psi = heading_fusion_apprentice[j]*np.pi/180.0
    R = SDOF.R123(phi,theta,psi)
    #%compute R such that v(inertial) = R v(body)
    vbody = np.asarray([velocity_apprentice_deriv_filter[j],0,0])
    vinertial = np.matmul(R,vbody)
    x_apprentice_deriv_gps[j] = vinertial[0]
    y_apprentice_deriv_gps[j] = vinertial[1]
    z_apprentice_deriv_gps[j] = vinertial[2]

    ##Need to compute Velocity of pitot in body frame
    #oh duh.... it's just vpitot = [vmeasured,0,0] since the pitot is always forward

    p = p_app[j]*np.pi/180.0
    q = q_app[j]*np.pi/180.0
    r = r_app[j]*np.pi/180.0

    #Angular Rate Substraction
    vx_angular = pitot_speed_filtered[j] - (-r*ry + q*rz)
    vy_angular = 0.0 - (r*rx  - p*rz)
    vz_angular = 0.0 - (-q*rx + p*ry)

    #Angular Rate Substraction with FP4
    vx_angular4 = VX_interp[j] - (-r*ry4 + q*rz4)
    vy_angular4 = VY_interp[j] - (r*rx4  - p*rz4)
    vz_angular4 = VZ_interp[j] - (-q*rx4 + p*ry4)

    #Rotate to Body Frame
    vbody = np.asarray([vx_angular,vy_angular,vz_angular])
    vinertial = np.matmul(R,vbody)

    vbody4 = np.asarray([vx_angular4,vy_angular4,vz_angular4])
    vinertial4 = np.matmul(R,vbody4)

    #Substract the xdot, ydot, zdot
    #Which to use? According to the plots the GPS ones look way better
    vatmx.append(vinertial[0]-x_apprentice_deriv_gps[j])
    vatmy.append(vinertial[1]-y_apprentice_deriv_gps[j])
    vatmz.append(vinertial[2]-z_apprentice_deriv_gps[j])

    #Substract the xdot, ydot, zdot
    #Which to use? According to the plots the GPS ones look way better
    vatmx4.append(vinertial4[0]-x_apprentice_deriv_gps[j])
    vatmy4.append(vinertial4[1]-y_apprentice_deriv_gps[j])
    vatmz4.append(vinertial4[2]-z_apprentice_deriv_gps[j])
        
print 'Computed Derivative of X and Y and Z and also computed atmospheric velocity'

vatmx = np.asarray(vatmx)
vatmy = np.asarray(vatmy)
vatmz = np.asarray(vatmz)

vatm = np.sqrt(vatmx**2 + vatmy**2 + vatmz**2)

app_pitot_OneMin = M.averages(time_apprentice,vatm,1)

vatmx4 = np.asarray(vatmx4)
vatmy4 = np.asarray(vatmy4)
vatmz4 = np.asarray(vatmz4)

vatm4 = np.sqrt(vatmx4**2 + vatmy4**2 + vatmz4**2)

pitot4_OneMin = M.averages(time_apprentice,vatm4,1)


##############PLOT EVERYTHING

print 'Start plotting'

pp = PDF(0,plt)

FONTSIZE = 12
SETXLIM = 0
if SETXLIM:
    x0 = 14.0 + 6.0/60.0
    xf = 14.0 + 22.0/60.0

####LATITUDE AND LONGITUDE
plti = myplot.plottool(FONTSIZE,'Time (hr)','Latitude (deg)','Latitude vs Time')
plti.plot(time_apprentice,latitude_apprentice,label='Apprentice')
plti.plot(time_pitot,latitude_pitot,label='FP4')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Longitude (deg)','Longitude vs Time')
plti.plot(time_apprentice,longitude_apprentice,label='Apprentice')
plti.plot(time_pitot,longitude_pitot,label='FP4')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Latitude (deg)','Longitude (deg)','Latitude vs. Longitude')
plti.plot(latitude_apprentice,longitude_apprentice)
#plti.plot(latitude_pitot,longitude_pitot,label='FP4')
plti.legend()
pp.savefig()

print 'plot...'

###X AND Y AND Z
plti = myplot.plottool(FONTSIZE,'Time (hr)','X (m)','X vs Time')
plti.plot(time_apprentice,x_apprentice,label='Apprentice')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Y (m)','Y vs Time')
plti.plot(time_apprentice,y_apprentice,label='Apprentice')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','Z (m)','Z vs Time')
plti.plot(time_apprentice,z_apprentice,label='Apprentice')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'X (m)','Y (m)','X vs Y')
plti.plot(x_apprentice,y_apprentice,label='Apprentice')
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','X dot (m/s)','Xdot vs Time')
plti.plot(time_apprentice,x_apprentice_deriv_filter,label='Derivative')
plti.plot(time_apprentice,x_apprentice_deriv_gps,label='GPS')
if SETXLIM:
    myplot.xlim_auto(x0,xf,time_apprentice,x_apprentice_deriv)
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Y dot (m/s)','Ydot vs Time')
plti.plot(time_apprentice,y_apprentice_deriv_filter,label='Derivative')
plti.plot(time_apprentice,y_apprentice_deriv_gps,label='GPS')
if SETXLIM:
    myplot.xlim_auto(x0,xf,time_apprentice,y_apprentice_deriv)
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Z dot (m/s)','Zdot vs Time')
plti.plot(time_apprentice,z_apprentice_deriv_filter,label='Derivative')
plti.plot(time_apprentice,z_apprentice_deriv_gps,label='GPS')
if SETXLIM:
    myplot.xlim_auto(x0,xf,time_apprentice,z_apprentice_deriv)
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','Total Velocity (m/s)','Total Velocity vs Time')
plti.plot(time_apprentice,velocity_apprentice_deriv_filter,label='Derivative of Position')
plti.plot(time_apprentice,velocity_apprentice_gps,label='GPS')
#plti.plot(time_apprentice,pitot_speed,label='Pitot Speed')
plti.plot(time_apprentice,pitot_speed_filtered,label='Pitot')
plti.plot(time_pitot,alg_v_filter,label='FP4')
plti.legend(loc='best')
pp.savefig()

###ROLL AND PITCH OF APPRENTICE
plti = myplot.plottool(FONTSIZE,'Time (ms)','Angle (deg)','Roll vs Time')
plti.plot(time_apprentice,roll_apprentice,label='Roll')
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (ms)','Angle (deg)','Pitch vs Time')
plti.plot(time_apprentice,pitch_apprentice,label='Pitch')
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Angle (deg)','Roll and Pitch vs Time')
plti.plot(time_apprentice,roll_apprentice,label='Roll')
plti.plot(time_apprentice,pitch_apprentice,label='Pitch')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Angle (deg)','Yaw vs Time')
plti.plot(time_apprentice,yaw_apprentice,label='IMU')
plti.plot(time_apprentice,heading_apprentice,label='GPS')
plti.plot(time_apprentice,heading_fusion_apprentice,label='GPS+IMU')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend(loc='best')
pp.savefig()

###Gyro Data
plti = myplot.plottool(FONTSIZE,'Time (hr)','Angular Rate (deg/s)','Angular Rate Data')
plti.plot(time_apprentice,p_app,label='GyroX')
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','Angular Rate (deg/s)','Angular Rate Data')
plti.plot(time_apprentice,q_app,label='GyroY')
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','Angular Rate (deg/s)','Angular Rate Data')
plti.plot(time_apprentice,r_app,label='GyroZ')
plti.legend()
pp.savefig()

print 'plot...'

###Data Points
plti = myplot.plottool(FONTSIZE,'Time (hr)','Raw Measured Velocity (m/s)','Measured Velocity')
plti.plot(time_pitot,pitot_signal_1, label='North Sensor')
plti.plot(time_pitot,pitot_signal_2, label='East Sensor')
plti.plot(time_pitot,pitot_signal_3, label='West Sensor')
plti.plot(time_pitot,pitot_signal_4, label='South Sensor')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend(loc='best')
pp.savefig()

print 'plot...'

##Plot scalar speed and direction from Algorithm
plti = myplot.plottool(FONTSIZE,'Time (hr)','Scalar Wind Speed (m/s)','Algorithm')
plti.plot(time_pitot,alg_v)
plti.plot(time_pitot,alg_v_filter,label='Filtered')
if SETXLIM:
    plti.set_xlim([x0,xf])
# plti.plot(time_apprentice,np.sqrt(x_apprentice_deriv**2 + y_apprentice_deriv**2))
# plti.plot(time_pitot,pitot_signal_1, label='East Sensor')
# plti.plot(time_pitot,pitot_signal_2, label='South Sensor')
# plti.plot(time_pitot,pitot_signal_3, label='West Sensor')
# plti.plot(time_pitot,pitot_signal_4, label='North Sensor')
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Direction (deg)','Algorithm')
plti.plot(time_pitot,alg_psi)
plti.plot(time_pitot,alg_psi_filter,label='Filtered')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

###Plot VX, VY since VZ is zero
plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Speed (m/s)','Algorithm')
plti.plot(time_pitot,VX, label='VX')
plti.plot(time_apprentice,VX_interp, label='VX interp')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

print 'plot...'

plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Speed (m/s)','Algorithm')
plti.plot(time_pitot,VY, label='VY')
plti.plot(time_apprentice,VY_interp, label='VY interp')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

#Kinematic Relationships
plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Speed (m/s)','Output from Kinematic')
plti.plot(time_apprentice,vatmx, label='VX')
plti.plot(time_apprentice,vatmx4,label='VX4')
if SETXLIM:
    #plti.set_xlim([x0,xf])
    myplot.xlim_auto(x0,xf,time_apprentice,vatmx)
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Speed (m/s)','Output from Kinematic')
plti.plot(time_apprentice,vatmy, label='VY')
plti.plot(time_apprentice,vatmy4,label='VY4')
if SETXLIM:
    #plti.set_xlim([x0,xf])
    myplot.xlim_auto(x0,xf,time_apprentice,vatmy)
plti.legend()
pp.savefig()

plti = myplot.plottool(FONTSIZE,'Time (hr)','Wind Speed (m/s)','Output from Kinematic')
plti.plot(time_apprentice,vatmz, label='VZ')
plti.plot(time_apprentice,vatmz4,label='VZ4')
if SETXLIM:
    plti.set_xlim([x0,xf])
plti.legend()
pp.savefig()

###Final Plots
plti = myplot.plottool(10,'Time (hr)','Wind Speed (m/s)','Scalar Wind Speed Comparison')
#plti.plot(scalar_oneminute[0],scalar_oneminute[1], label='FP4V One Minute Average')
#plti.plot(time_apprentice,vatm,label='Apprentice Pitot Probe')
plti.plot(anemometer_OneMin[0],anemometer_OneMin[1],label='Anemometer One Minute Average')
plti.plot(app_pitot_OneMin[0],app_pitot_OneMin[1],label='Apprentice Pitot One Minute Average')
plti.plot(pitot4_OneMin[0],pitot4_OneMin[1],label='FP4 One Minute Average')
plti.legend(loc='best')
pp.savefig()

pp.close()
