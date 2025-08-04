#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from math import *
from matplotlib.backends.backend_pdf import PdfPages
import sys
import os
#from fileinput import filename


def process_pitot_data(inputfilename,debugmode=0):
    time_truth = np.linspace(0,140,100)
    speed_truth = np.zeros((100))
    #Wind tunnel Hz = [10,20,30,40,50]
    #Wind tunnel speed = [0.5,1.0,2.0,2.7,3.3]
    # 10, 2.0,1.0
    # 20,4.5, 2.5
    # 30,7.5/5.0, 4.0
    # 40,10.0/7.5,6.0
    #Confidence interval
    #speed_truth is easily off by 0.5 m/s
    #Generate "Truth" Signal - only for windtunnel calibration
    data = np.asarray([1.0,2.5,4.0,6.0,7.5])-0.5
    for x in range(0,len(time_truth)):
        if time_truth[x] < 20:
            speed_truth[x] = 0
        elif time_truth[x] < 40:
            speed_truth[x] = data[0]
        elif time_truth[x] < 60:
            speed_truth[x] = data[1]
        elif time_truth[x] < 80:
            speed_truth[x] = data[2]
        elif time_truth[x] < 100:
            speed_truth[x] = data[3]
        elif time_truth[x] < 120:
            speed_truth[x] = data[4]
        elif time_truth[x] < 140:
            speed_truth[x] = 0


    #Read data from file
    print 'Loading File...'

    #file = open('Windtunnel_Calibration_Test.TXT')
    #file = open('AIRSPEED.TXT')
    pitotdata = open(inputfilename)
    #file = open('Fan_Calibration.TXT')

    time = []
    raw = []
    
    lenfile = 0

    for line in pitotdata:
        lenfile+=1
        #print len(line)
        if len(line) > 2 and line[0] != 'D':
            row = line.split(' ')
            #print row
            time.append(np.float(row[0])/1000) #don't forget to convert to float
            raw.append(np.float(row[1]))

    time_np = np.array(time)
    raw_np = np.array(raw)

    print 'File Loaded'

    ###CONVERT RAW SIGNAL TO VOLTS - The raw signal is a 10-bit register
    ###so you need to convert it to volts. 2^10 = 1024 so basically 1024 =
    ###5 volts - it's completely linear
    voltage = raw_np*(5.0/1023.0); 

    #//2.5 volts should equal zero kPa. Should probably just calibrate
    #this every time instead of storing a random number
    #Apprarently this gives pressure in kPa which means the voltage is a
    #function of pressure
    t = time_np[0]
    meanV = 0;
    numData = 0;
    while t < 10:
        meanV += voltage[numData]
        numData += 1
        t = time_np[numData]
        
    meanV = meanV/numData

    #We need to substract off like the first 5 seconds of data instead of
    #using just a saved number
    print 'Calibrated Voltage = ',meanV
    pressure_kpa = voltage-meanV;

    ####Q is kPa converted to atmospheres
    ####REVISIT REVISIT
    #This pressure term should get pulled from iMet
    #data
    pressure_atm = pressure_kpa/101.325;

    ####This equation here comes from bernoulli
    k = 5*((pressure_atm+1.0)**(2.0/7.0)-1);

    #There is a potential here for
    #k to be less than 0. If that happens, the sqrt goes imaginary
    #Thus we need to add in a fix here
    for x in range(0,len(k)):
        if k[x] < 0.0:
            k[x] = 0.0

    #This is the rest of the equation from bernoulli. 343.2 is the speed of
    #REVISIT REVISIT
    #sound at sea-level
    #Sqrt(gamma*R*T) - Replace with this!
    #T is in Kelvin
    #R is 286 ideal gas constant
    #Gamma is the adiabatic index = 1.4
    tempC = 20
    tempK = tempC + 273.15
    a_inf = sqrt(1.4*286*tempK)
    airspeed_ms = a_inf*k**(0.5)

    print 'Filtering Signal...'

    ##Run signal through a complimentary filter
    sigma = 0.03
    airspeed_ms_filtered = np.zeros(len(airspeed_ms))
    airspeed_ms_filtered[0] = airspeed_ms[0]
    for idx in range(0,len(airspeed_ms)-1):
        airspeed_ms_filtered[idx+1] = (1-sigma)*airspeed_ms_filtered[idx] + sigma*airspeed_ms[idx]

    print 'Filter Complete'

    #Because conversion from Voltage to speed
    #is still noisy we need to calibrate one more
    #time
    t = time_np[0]
    meanU = 0;
    numData = 0;
    while t < 10:
        meanU += airspeed_ms_filtered[numData]
        numData += 1
        t = time_np[numData]

    airspeed_ms_filtered = airspeed_ms_filtered - meanU/numData

    #RAW SIGNAL
    if debugmode == 1:
        plt.figure()
        plt.plot(time_np,raw_np)
        plt.xlabel('Time (sec)')
        plt.ylabel('Raw Bits (0-1023)')
        plt.grid()
        pp.savefig()
        
        #Voltage
        plt.figure()
        plt.plot(time_np,voltage)
        plt.xlabel('Time (sec)')
        plt.ylabel('Raw Voltage (V)')
        plt.grid()
        pp.savefig()

        #Voltage
        plt.figure()
        plt.plot(time_np,voltage-meanV)
        plt.xlabel('Time (sec)')
        plt.ylabel('Scaled Voltage (V)')
        plt.grid()
        pp.savefig()

    #Return Data
    return [time_np,airspeed_ms_filtered]

if __name__ == "__main__":

    print 'Creating Plots...'

    ###SAVE FIGS
    os.system('rm plots.pdf')
    pp = PdfPages('plots.pdf')

    print 'Processing Pitot Probe File'
    #inputfilename = 'ZEIGLER_PARK1.TXT'
    inputfilename = 'AIRSPEED.TXT'
    #inputfilename = 'SHELBYHALL.TXT'
    data = process_pitot_data(inputfilename,1)
    time_np = data[0]
    airspeed_ms_filtered = data[1]

    ##PROCESSED DATA
    plt.figure()
    #plt.plot(time_truth,speed_truth)
    # plt.plot(time_np,airspeed_ms,color='green')
    plt.plot(time_np,airspeed_ms_filtered,color='red')
    plt.xlabel('Time (sec)')
    plt.ylabel('Speed (m/s)')
    plt.grid()
    pp.savefig()

    #CLOSE FILE
    pp.close()

    print 'Plots Saved'

    #AND THEN USE EVINCE TO OPEN PDF if on linux
    if sys.platform == 'linux2':
        os.system('evince plots.pdf &')



    # print time_np
    # print airspeed_ms_filtered
    



    
    

