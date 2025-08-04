#!/usr/bin/python3
import numpy as np
import sys
sys.path.append('/home/carlos/Git_Repos/Github/HIL/')
from IMU.mpu9250 import MPU9250
from GPS.gps import GPS
sys.path.append('/home/carlos/Git_Repos/Github/Python/datalogger')
from datalogger import Datalogger

## Alright Let's generate some synthetic data sets by assuming a drone has
## the following sensors: IMU, GPS, Anemometer, Barometer, Thermistor/RH sensor, pyranometer, rain gauge and a camer

#######SET PARAMS
TEND = 3600.0 #time of data set
TS = 60.0 ##PERIOD IN SECONDS
FS = 1/TS ##Sampling rate
TOD = 0.5 ##TIME OF DAY IN PERCENT FROM 0-1
WRPY = 3.0 ##angular frequency of vehicle
PX = 10.0 ##PHASE SHIFT OF RPY
PY = 3.0 
PZ = -4.0
OX = 0.0 ###OFFSETS OF RPY
OY = 0.0
OZ = 30.0 
VEL = 20.0 ##VELOCITY OF VEHICLE
METW = 0.4 ##ANGULAR VELOCITY OF MET SENSORS
TEMP = 30.0 #TEMPERATURE
TEMPVAR = 10.0 ##VARIATION IN TEMP
RH = 40.0 ##RELATIVE HUMIDITY
RHVAR = 10.0 # VARIATION IN HUMIDITY
PRESS = 950. ##PRESSURE
PRESSVAR = 100. ##PRESSRUE VARIATION
WIND = 10.0 ##WINDSPEED
WINDVAR = 5.0 ##WINDSPEED VARIATION
WINDDIR = 135.0 ##WINDDIRECTION
WINDDIRVAR = 100.0 ##WINDDIRECTION VARIATION
RAIN = 0.2  ##RAIN FALL
SOLAR = 0.5 ##SOLAR RADIATION
CAMID = 42 ##CAMID

## For now let's just make this simple and assume we're sampling at fs HZ
Ts = 1.0/FS
clk = np.arange(0,TEND+0.1,Ts)
gpsclk = clk + TOD*86400.0

## IMU SENSE
## SET RPY AND GET IMU
roll = 0*clk + np.sin(WRPY*clk + PX) + OX
pitch = 0*clk + np.cos(WRPY*clk + PY) + OY
yaw = 0*clk + np.sin(WRPY*clk + PZ) + OZ
##To get gyro take a derivative of rpy
gx = (roll[1:]-roll[0:-1])/(clk[1:]-clk[0:-1])
gx = np.hstack((0,gx))
gy = (pitch[1:]-pitch[0:-1])/(clk[1:]-clk[0:-1])
gy = np.hstack((0,gy))
gz = (yaw[1:]-yaw[0:-1])/(clk[1:]-clk[0:-1])
gz = np.hstack((0,gz))
##To get ax,ay,az you need to extract using the imu utility
ax = 0*clk
ay = 0*clk
az = 0*clk
imu = MPU9250()
mx = 0*clk
my = 0*clk
mz = 0*clk
for i in range(0,len(clk)):
	aB,mB = imu.convertRPY2RAW(roll[i],pitch[i],yaw[i])
	ax[i] = aB[0]
	ay[i] = aB[1]
	az[i] = aB[2]
	mx[i] = mB[0]
	my[i] = mB[1]
	mz[i] = mB[2]
"""This is if you want to set the raw IMU data and RPY
ax = 0*clk
ay = 0*clk
az = 0*clk + 9.81
gx = 0*clk
gy = 0*clk
gz = 0*clk
mx = 0*clk - 27.13 #Values taken from bench experiment
my = 0*clk - 13.66
mz = 0*clk + 296.88
#To get rpy we use ax,ay,az,gx,gy,gz and mx,my,mz
roll = 0*clk
pitch = 0*clk
yaw = 0*clk
imu = MPU9250()
for i in range(0,len(clk)):
	ai = [ax[i],ay[i],az[i]]
	gi = [gx[i],gy[i],gz[i]]
	mi = [mx[i],my[i],mz[i]]
	rpy = imu.imufusion(ai,gi,mi)
	roll[i] = rpy[0]
	pitch[i] = rpy[1]
	yaw[i] = rpy[2]
"""

##GPS SENSE
gps = GPS()
VX = 0*clk + VEL*np.cos(yaw*np.pi/180.0)
VY = 0*clk + VEL*np.sin(yaw*np.pi/180.0)
VZ = 0*clk
X = VX*clk 
Y = VY*clk
Z = VZ*clk
lat = 0*clk
lon = 0*clk
alt = 0*clk
for i in range(0,len(clk)):
	lat[i],lon[i],alt[i] = gps.convertXYZ2LATLON(X[i],Y[i],Z[i])

##MET SENSORS
temp = 0*clk + TEMP + TEMPVAR*np.sin(METW*clk)
rh = 0*clk + RH + RHVAR*np.sin(METW*clk)
pressure = 0*clk + PRESS + PRESSVAR*np.sin(METW*clk)
windspeed = np.sqrt(VX**2+VY**2+VZ**2) + WIND + WINDVAR*np.sin(METW*clk)
direction = np.arctan2(VY,VX) + WINDDIR + WINDDIRVAR*np.sin(METW*clk)
rain = 0*clk + RAIN
solar = 0*clk + SOLAR
cam = 0*clk + CAMID

##Now we concat all files
## POD1
## CLK - CPU Time
## IMU - Accel, Gyro
## GPS - GPS Time, LAT, LON, ALT, VX, VY, VZ
## MAG - Mag
## ANEM - Windspeed / Dir (note this includes the speed of the vehicle)
## BARO - Pressure in mb
## TEMP/RH - Temperature and Relative Humidity
## PYRO - Solar Radiation
## RAIN - Rain in mm of rainfall
## CAM - ID
header1 = ['CLK','AX','AY','AZ','GX','GY','GZ','GPS TIME','LAT','LON','ALT','VX','VY','VZ','MX','MY','MZ','WINDSPEED','DIRECTION','PRESSURE','TEMPERATURE','RELATIVE HUMIDITY','SOLAR RADIATION','RAINFALL','CAM ID']
pod1 = np.vstack((clk,ax,ay,az,gx,gy,gz,gpsclk,lat,lon,alt,VX,VY,VZ,mx,my,mz,windspeed,direction,pressure,temp,rh,solar,rain,cam))

## POD2
## CLK - CPU Time
## IMU - Accel, Gyro, Mag, RPY
## GPS - GPS Time, LAT, LON, ALT, VX, VY, VZ
## BARO - Pressure
## GPS2 - GPS Time, LAT, LON, ALT, VX, VY, VZ
## ANEM - Windspeed / Dir (note this includes the speed of the vehicle)
## BARO2 - Pressure in mb
## TEMP/RH - Temperature and Relative Humidity
header2 = ['CLK','AX','AY','AZ','GX','GY','GZ','MX','MY','MZ','ROLL','PITCH','YAW','GPS TIME','LAT','LON','ALT','VX','VY','VZ','PRESSURE','GPS TIME','LAT','LON','ALT','VX','VY','VZ','WINDSPEED','DIRECTION','PRESSURE','TEMPERATURE','RELATIVE HUMIDITY']
pod2 = np.vstack((clk,ax,ay,az,gx,gy,gz,mx,my,mz,roll,pitch,yaw,gpsclk,lat,lon,alt,VX,VY,VZ,pressure,gpsclk,lat,lon,alt,VX,VY,VZ,windspeed,direction,pressure,temp,rh))

## POD3
## CLK - CPU Time
## IMU - Accel, Gyro, Mag, RPY
## GPS - GPS Time, LAT, LON, ALT, VX, VY, VZ
## ANEM - Windspeed / Dir (note this includes the speed of the vehicle)
## BARO - Pressure in mb
## TEMP/RH - Temperature and Relative Humidity
header3 = ['CLK','AX','AY','AZ','GX','GY','GZ','MX','MY','MZ','ROLL','PITCH','YAW','GPS TIME','LAT','LON','ALT','VX','VY','VZ','WINDSPEED','DIRECTION','PRESSURE','TEMPERATURE','RELATIVE HUMIDITY']
pod3 = np.vstack((clk,ax,ay,az,gx,gy,gz,mx,my,mz,roll,pitch,yaw,gpsclk,lat,lon,alt,VX,VY,VZ,windspeed,direction,pressure,temp,rh))

outarray = np.vstack((pod1,pod2,pod3))
outarray = np.transpose(outarray)
#print(outarray)
##Ok now we write everything to a file
logger = Datalogger()
logger.findfile('./data/','.csv')
logger.open()
##First print the header
header = header1 + header2 + header3
logger.println(header)
for i in range(0,len(clk)):
	outrow = outarray[i,:]
	logger.println(outrow)
	#print(outrow)
logger.close()