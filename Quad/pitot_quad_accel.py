#!/usr/bin/python

# Geophysical_Sampling Plot mesonet, pitot, imet and quad

import sys
#Import pitot module
sys.path.append('FASTPitot/')
import pitot as FP
#Import Quad module
sys.path.append('Quad/')
import quad as Q
#Import extra stuff
import gps as GPS
import mymath as M
from pdf import PDF
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    #Input Arguments
    if len(sys.argv) < 5:
        print 'Need QuadFile,PitotFile,Num_pitots,GPSOFFON'
        sys.exit()
    else:
        quadFile = sys.argv[1]
        pitotFile = sys.argv[2]
        numPitots = int(sys.argv[3])
        NOGPS = int(sys.argv[4])

    ##Setup PDF
    SHOWPLOTS = 0 #0 = PDF, 1 = show plots using plt.show()
    pp = PDF(SHOWPLOTS,plt)

    ##Get quad data
    quad_data = Q.get_quad_data(quadFile)

    #Get Pitot Data
    CAL_TIMES = [-99,0] #Default to zero
    sigma_pitot = 0.03 #closer to zero is more filtering
    #data_pitot_all = FP.get_pitot_data(pitotFile,numPitots,sigma_pitot,CAL_TIMES,0,pp,NOGPS)
    data_pitot_all = FP.get_pitot_simple(pitotFile,numPitots)
    
    #Get dictionary
    #print(quad_data[-1])

    IMUDATA = quad_data[3]

    #Get IMU Directory
    #print dir(IMUDATA)

    #Create Plot
    figure1 = plt.figure()
    plt1 = figure1.add_subplot(1,1,1)

    #Get pitot dictionary
    #print data_pitot_all[-1]

    pitot_data = data_pitot_all[1]
    #print pitot_data[-1]
    time_pitot = pitot_data[0]
    raw_data = pitot_data[3]
    #print len(time_pitot),len(raw_data[:,0])
    plt1.plot(time_pitot,raw_data[:,0],label='Raw Pitot Bits')

    ##Compute scale factor for pitot
    scale_factor_pitot = np.max(raw_data[:,0])-np.min(raw_data[:,0])
    IMUnp = np.array(IMUDATA.AccY)

    ##Start and end point
    x0 = 523
    xf = 528
    timeIMUnp = np.array(IMUDATA.timeMS_IMU)
    # l0 = np.where(timeIMUnp>x0)
    # l0 = l0[0][0]
    # lf = np.where(timeIMUnp>xf)
    # lf = lf[0][0]
    l0 = 0
    lf = len(IMUDATA.timeMS_IMU)
    print l0,lf
    scale_factor_IMU = np.max(IMUnp[l0:lf])-np.min(IMUnp[l0:lf])
    scale_factor = scale_factor_pitot/scale_factor_IMU

    print scale_factor_pitot,scale_factor_IMU,scale_factor

    #Plot Quad Accel
    #Shift and scale AccZ
    IMUscaled = 2*(IMUnp - IMUnp[0])*scale_factor + float(raw_data[1,0])
    plt1.plot(np.array(IMUDATA.timeMS_IMU)+480,IMUscaled,label='Scaled Accelerometer')
    plt1.grid()

    ##XLIMIT
    plt1.set_xlim([x0,xf])
    plt1.set_ylim([np.min(raw_data[:,0]),np.max(raw_data[:,0])])
    plt1.set_xlabel('Time (sec)')
    plt1.set_ylabel('Raw Bits and Scaled Acceleration (m/s^2)')
    plt1.legend()

    #Finish plotting
    pp.savefig()
    pp.close()
