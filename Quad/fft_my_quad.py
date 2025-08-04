#!/usr/bin/python

import numpy as np
import mymath as M
import matplotlib.pyplot as plt
import plotting as P
from pdf import *
import quad as Q
import sys

pp = PDF(0,plt)

fileName = sys.argv[1]

##Ok first need to pull in the data
quad_data = Q.get_quad_data(fileName)

##Get IMU stucture
IMUdata = quad_data[3]
baroRead = quad_data[0]

#Plot the Gyro Data
#Using File = ???
#IMUdata.plot_IMU(400,800,pp,baroRead)

#Using File = Sys_ID_Flight.log from UAH 11/17/2017
x0 = 40
xf = 60
IMUdata.plot_IMU(x0,xf,pp,baroRead)

##Choose Either X,Y or Z
vib = IMUdata.AccX

#Now that we've plotted it let's run the FFT
i = np.where( (IMUdata.timeMS_IMU > x0) & (IMUdata.timeMS_IMU < xf) )[0]
nmax = 400
d,an,bn,iters,freq = M.fft(vib[i],IMUdata.timeMS_IMU[i],nmax,1,pp)

#Test a LowPas Filter
##Based on data set filter to 0.5 Hz
fpass = 0.25
outY,outX = M.LowPass(vib[i],IMUdata.timeMS_IMU[i],2*np.pi*fpass)

plt3 = P.plottool(12,'Time (sec)','Acceleration (m/s^2)','Low Pass Results')
plt3.plot(IMUdata.timeMS_IMU[i],vib[i],color='blue',label='Raw Signal')
plt3.plot(IMUdata.timeMS_IMU[i],outY,'r--',label='Filtered Data')
plt3.legend()
pp.savefig()

pp.close()
