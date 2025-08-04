#!/usr/bin/python

import sys
sys.path.append('Quad/')
sys.path.append('Anemometer/')
sys.path.append('FASTPitot/')
from pitot import create_PTH_plots
from anemometer import get_anemometer_data
from anemometer import create_anemometer_plots
import quad as Q
import mymath as M
from pdf import PDF
from mymath import LowPass
from gps import *
from math import sqrt
#from pitot import create_PTH_plots


import matplotlib.pyplot as plt

import numpy as np


if __name__ == "__main__":
    
    #Setup the PDf
    SHOWPLOTS = 0 #0 = PDF, 1 = show plots using plt.show()
    pp = PDF(SHOWPLOTS,plt)
    
    quadFile = sys.argv[1]
    anemFile = sys.argv[2]

    ##Grab quad data
    quad_data = Q.get_quad_data(quadFile)
    
    #print ('quad data loaded')
    
    ##now I only want to get the IMU data from the quad
    IMUDATA = quad_data[3]

    #plot acceleration in the x direction (pitch)
    figure1 = plt.figure()
    plt.plot((IMUDATA.timeMS_IMU),(IMUDATA.AccX),label = 'Unfiltered')
    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccX2,label = 'Unfiltered')
    plt.grid()
    plt.ylim([-5,5])

    wc = 1.0 ###The smaller the number the more filtering
    [IMUDATA.AccX_Filtered,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccX,IMUDATA.timeMS_IMU,wc)

    wc = 0.3 ###The smaller the number the more filtering
    [IMUDATA.AccX_mean,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccX,IMUDATA.timeMS_IMU,wc)

    wc = 1.0 ###The smaller the number the more filtering
    [IMUDATA.AccX2_Filtered,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccX2,IMUDATA.timeMS_IMU,wc)

    wc = 0.3 ###The smaller the number the more filtering
    [IMUDATA.AccX2_mean,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccX2,IMUDATA.timeMS_IMU,wc)

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccX_Filtered,label='Filtered')

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccX_mean,label='Mean')

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccX2_Filtered,label='Filtered')

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccX2_mean,label='Mean')

    plt.legend()

    pp.savefig()

    #plot acceleration in the y direction (roll)
    figure2 = plt.figure()
    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccY,label = 'Unfiltered Y')
    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccY2,label = 'Unfiltered Y')

    ###filter the y direction acceleration data
    
    wc = 1.0 ###The smaller the number the more filtering
    [IMUDATA.AccY_Filtered,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccY,IMUDATA.timeMS_IMU,wc)

    wc = 0.3 ###The smaller the number the more filtering
    [IMUDATA.AccY_mean,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccY,IMUDATA.timeMS_IMU,wc)

    wc = 1.0 ###The smaller the number the more filtering
    [IMUDATA.AccY2_Filtered,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccY2,IMUDATA.timeMS_IMU,wc)

    wc = 0.3 ###The smaller the number the more filtering
    [IMUDATA.AccY2_mean,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccY2,IMUDATA.timeMS_IMU,wc)

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccY_Filtered,label='Filtered')

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccY_mean,label='Mean')

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccY2_Filtered,label='Filtered')

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccY2_mean,label='Mean')

    plt.legend()
    
    plt.grid()
             
    pp.savefig()

    ###plot acceleration in the z direction (altitude)
    figure3 = plt.figure()
    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccZ,label = 'Unfiltered Z')
    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccZ2,label = 'Unfiltered Z')

    wc = 1.0 ###The smaller the number the more filtering
    [IMUDATA.AccZ_Filtered,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccZ,IMUDATA.timeMS_IMU,wc)

    wc = 0.3 ###The smaller the number the more filtering
    [IMUDATA.AccZ_mean,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccZ,IMUDATA.timeMS_IMU,wc)

    wc = 1.0 ###The smaller the number the more filtering
    [IMUDATA.AccZ2_Filtered,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccZ2,IMUDATA.timeMS_IMU,wc)

    wc = 0.3 ###The smaller the number the more filtering
    [IMUDATA.AccZ2_mean,IMUDATA.timeMS_IMU_Filtered] = LowPass(IMUDATA.AccZ2,IMUDATA.timeMS_IMU,wc)

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccZ_Filtered,label='Filtered')

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccZ_mean,label='Mean')

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccZ2_Filtered,label='Filtered')

    plt.plot(IMUDATA.timeMS_IMU,IMUDATA.AccZ2_mean,label='Mean')

    plt.legend()

    
    plt.grid()
    plt.ylim([-2,2])
    pp.savefig()

    ###now use euler's method of integration on each acceleration to get the velocities
    #eulers mehtod is y1 = y0 + f(t0)*h where y = v(t), f = v(t) and h ~= 0.025 seconds
    velX = [0]
    #velX[0] = 0

    # for idx in IMUDATA.AccX: #<----you integrate the last point and you one more than you need
    #     currentvel = velX[-1] + idx*0.025
    #     velX.append(currentvel)
    # del(velX[-1])
    # print(len(velX),len(IMUDATA.timeMS_IMU))

    # ACCELERATION = TRUTH_SIGNAL + NOISE + BIAS(t) <- BIAS????
    # ACCELERATION_FILTERED = TRUTH_SIGNAL + BIAS(t)
    # ESTIMATOR ON HERE
    # CONTROL INPUTS(!!!) -> MODEL(??????) -> MODEL OUTPUT
    # MODEL_OUTPUT - SENSOR OUTPUT = BIAS

    meanAccX = np.mean(IMUDATA.AccX)

    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velX[-1] + (IMUDATA.AccX[x]-IMUDATA.AccX_mean[x])*h
        velX.append(nextvel)

    velX_Filtered = [0]
    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velX_Filtered[-1] + IMUDATA.AccX_Filtered[x]*h
        velX_Filtered.append(nextvel)

    #print(len(velX),len(IMUDATA.timeMS_IMU))

  

    velX2 = [0]

    meanAccX2 = np.mean(IMUDATA.AccX2)

    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velX2[-1] + (IMUDATA.AccX2[x]-IMUDATA.AccX2_mean[x])*h
        velX2.append(nextvel)

    velX2_Filtered = [0]
    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velX2_Filtered[-1] + IMUDATA.AccX2_Filtered[x]*h
        velX2_Filtered.append(nextvel)

    #print(len(velX2),len(IMUDATA.timeMS_IMU))

    #try to plot this and see how it looks
    figure4 = plt.figure()
    plt.plot(IMUDATA.timeMS_IMU,velX,label = 'lets go for gold')
    plt.plot(IMUDATA.timeMS_IMU,velX_Filtered,label = 'lets go for platinum?')
    plt.plot(IMUDATA.timeMS_IMU,velX2,label = 'lets go for gold again')
    plt.plot(IMUDATA.timeMS_IMU,velX2_Filtered,label = 'lets go for platinum? again?')
    plt.grid()
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Velocity (m/s)')
    plt.ylim([-5,5])
    pp.savefig()

    ##velocity in the y direction

    velY = [0]

    meanAccY = np.mean(IMUDATA.AccY)

    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velY[-1] + (IMUDATA.AccY[x]-IMUDATA.AccY_mean[x])*h
        velY.append(nextvel)

    velY_Filtered = [0]
    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velY_Filtered[-1] + IMUDATA.AccY_Filtered[x]*h
        velY_Filtered.append(nextvel)

    #print(len(velY),len(IMUDATA.timeMS_IMU))

  

    velY2 = [0]

    meanAccY2 = np.mean(IMUDATA.AccY2)

    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velY2[-1] + (IMUDATA.AccY2[x]-IMUDATA.AccY2_mean[x])*h
        velY2.append(nextvel)

    velY2_Filtered = [0]
    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velY2_Filtered[-1] + IMUDATA.AccY2_Filtered[x]*h
        velY2_Filtered.append(nextvel)

    #print(len(velY2),len(IMUDATA.timeMS_IMU))
    

    #try to plot this and see how it looks
    figure5 = plt.figure()
    plt.plot(IMUDATA.timeMS_IMU,velY,label = 'lets go for gold')
    plt.plot(IMUDATA.timeMS_IMU,velY_Filtered,label = 'lets go for platinum?')
    plt.plot(IMUDATA.timeMS_IMU,velY2,label = 'lets go for gold again')
    plt.plot(IMUDATA.timeMS_IMU,velY2_Filtered,label = 'lets go for platinum? again?')
    plt.grid()
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Velocity (m/s)')
    plt.ylim([-5,5])
    pp.savefig()

    ######z velocity #####


    velZ = [0]
    meanAccZ = np.mean(IMUDATA.AccZ)

    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velZ[-1] + (IMUDATA.AccZ[x]-IMUDATA.AccZ_mean[x])*h
        velZ.append(nextvel)

    velZ_Filtered = [0]
    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velZ_Filtered[-1] + IMUDATA.AccZ_Filtered[x]*h
        velZ_Filtered.append(nextvel)

    #print(len(velZ),len(IMUDATA.timeMS_IMU))

  

    velZ2 = [0]

    meanAccZ2 = np.mean(IMUDATA.AccZ2)

    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velZ2[-1] + (IMUDATA.AccZ2[x]-IMUDATA.AccZ2_mean[x])*h
        velZ2.append(nextvel)

    velZ2_Filtered = [0]
    for x in range(0,len(IMUDATA.timeMS_IMU)-1):
        h = IMUDATA.timeMS_IMU[x+1] - IMUDATA.timeMS_IMU[x]
        nextvel = velZ2_Filtered[-1] + IMUDATA.AccZ2_Filtered[x]*h
        velZ2_Filtered.append(nextvel)

    #print(len(velZ2),len(IMUDATA.timeMS_IMU))

    #try to plot this and see how it looks
    figure6 = plt.figure()
    plt.plot(IMUDATA.timeMS_IMU,velZ,label = 'lets go for gold')
    plt.plot(IMUDATA.timeMS_IMU,velZ_Filtered,label = 'lets go for platinum?')
    plt.plot(IMUDATA.timeMS_IMU,velZ2,label = 'lets go for gold again')
    plt.plot(IMUDATA.timeMS_IMU,velZ2_Filtered,label = 'lets go for platinum? again?')
    plt.grid()
    plt.legend()
    plt.xlabel('Time')
    plt.ylabel('Velocity (m/s)')
    plt.ylim([-5,5])
    pp.savefig()

    ###start plotting annemometer data


    #print('Processing Anemometer Probe File')

    if len(sys.argv) > 3:
        print(sys.argv)
        inputfilenames = [sys.argv[2],sys.argv[3]]
    else:
        inputfilenames = [sys.argv[2]]

    #PROCESS ANEMOMETER AND GPS DATA
    sigma = 0.03 #Closer to 0 means more filtering
    data_all = []
    for x in range(0,len(inputfilenames)):
        inputfilename = inputfilenames[x]
        data = get_anemometer_data(inputfilename,sigma,1,pp) #1 = debugmode on, if debug mode is on you need to send pp
        data_all.append(data)
        print(data_all[-1]) #to see directory
        data_gps = data[0]
        data_anemometer = data[1]

        #Anemometer Data - Remember you can just print data_anemometer[-1] to see where everything is
        print(data_anemometer[-1])
        # tot_time_sec_zero = data[0]
        # windspeed = data[1]
        # airspeed_ms = data[2]
        # airspeed_ms_filtered = data[3]

        #Create GPS Plots
        print(data_gps[-1])
        print("GPS Start = ",data_gps[2][0])
        print("GPS End = ",data_gps[2][-1])
        # gps_data needs to be like this
        # lat_vec_np = data[0]
        # lon_vec_np = data[1]
        # tot_time_gps = data[2]
        # x_vec_np = data[3]
        # y_vec_np = data[4]
        # alt_vec_np = data[5]
        FP_GPS_END = data_gps[2][-1]
        FP_GPS_START = data_gps[2][0]
        del_min = np.ceil((FP_GPS_END-FP_GPS_START)*60.0/10.0) #number of minutes

        #This will just plot one data stream at a time
        create_gps_plots(data_gps,del_min,pp,False) #this plots it

        #Make this 1 data stream as well
        create_anemometer_plots(data_anemometer,pp)

    figureW = plt.figure()
    pltW = figureW.add_subplot(1,1,1)

    data_PTH_all = []
    data_gps_all = []
    for x in range(0,len(inputfilenames)):
        data_x = data_all[x]

        data_gps = data_x[0]
        data_anemometer = data_x[1]
        data_PTH = data_x[2]

        data_PTH_all.append(data_PTH)
        data_gps_all.append(data_gps)
        
        ##Plotting windspeed as function of GPS time
        time_gps_np = data_gps[2]
        windspeed = data_anemometer[1]
        airspeed_ms_filtered = data_anemometer[3]

        time_vec_HHMM,xticks = HHMM_Format(time_gps_np,del_min)

        #1 Minute averages
        avg = M.averages(time_gps_np,airspeed_ms_filtered,1)
        
        pltW.plot(time_gps_np,airspeed_ms_filtered,label='Filtered Airspeed')
        pltW.plot(avg[0],avg[1],marker = 's',label='One Minute Averages')

    airspeed_ms_filtered0 = data_all[0][1][3]
    #airspeed_ms_filtered1 = data_all[1][1][3]
    airspeed_ms0 = data_all[0][1][2]
    #airspeed_ms1 = data_all[1][1][2]
    
    time_anem = data_all[0][1][0]
    time_gps_np1 = data_all[0][0][2]
    
    pltW.set_xticks(xticks) 
    pltW.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([time_gps_np[0],time_gps_np[-1]])    
    pltW.set_xlabel('Time (HH:MM)')
    pltW.set_ylabel('Windspeed, m/s')
    pltW.legend()
    
    pltW.grid()
    pp.savefig()

    #Create PTH Plots
    #let's print the PTH directory
    #print(data_PTH_all[0][-1])
    create_PTH_plots(data_PTH_all,data_gps_all,pp)

    #in order to get the resultant velocity of the quad to subtract off the anemometer data we need to take the square root of the squares of the x and y velocities
    
    
    velX1_np = np.asarray(velX)
    velY1_np = np.asarray(velY)
    velX2_np = np.asarray(velX2)
    velY2_np = np.asarray(velY2)

    velX_np = (velX1_np + velX2_np)/2.0
    velY_np = (velY1_np + velY2_np)/2.0
    

    resultant_vel = np.sqrt(velX_np**2+velY_np**2)
    
    
    #now this should be the resultant velocity?? Maybe?
    #so plot it
    figure8 = plt.figure()

    plt.plot(IMUDATA.timeMS_IMU,resultant_vel,label = 'Resultant')
    plt.plot(IMUDATA.timeMS_IMU,velX_np,label = 'Filtered X velocity')
    plt.plot(IMUDATA.timeMS_IMU,velY_np,label = 'Filtered Y velocity')
    plt.grid()
    plt.legend()
    pp.savefig()

    #next up is to subtract the resultant velocity off of the anemometer winds

    #the problem is that the anemometer data and the IMU data is different lengths
    #in order to fix this we have to use np.interp to linearly interpolate the data

    time = np.linspace(0,IMUDATA.timeMS_IMU[-1],len(IMUDATA.timeMS_IMU))

    #anem_ground = np.interp(time,len(avg[0])+1,avg[0])
    print time_anem[0]
    print time_anem[-1]
    print time[0]
    print time[-1]

    #I'm stumped 
    anem_long = np.interp(time,time_anem,airspeed_ms0)
    #anem_ground = np.interp(time,time_gps_np1,airspeed_ms1)
    
    real_airspeed = anem_long - (resultant_vel)

    figure9 = plt.figure()

    plt.plot(IMUDATA.timeMS_IMU,real_airspeed,label = 'this should be zero')
    #plt.plot(IMUDATA.timeMS_IMU,anem_ground, label = 'Tower anemometer')
    plt.grid()
    plt.legend()
    pp.savefig()
              
    pp.close()

   

