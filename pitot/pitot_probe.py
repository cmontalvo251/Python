#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import plotting as P
import sys
import csv
from gps import *
from pdf import *
from copy import deepcopy
from mymath import LowPass,Complimentary
#from fileinput import filename

class Pitot():
    def __init__(self,time,raw_bits,fileName):
        self.raw_bits = raw_bits
        self.time = time
        self.fileName = fileName
        self.WIND = None

    def plot_processed_bits(self,pp):
        plti = P.plottool(12,'Time (sec)','Bits','Pitot Probe File = '+self.fileName)
        plti.plot(self.time,self.raw_bits,label='Raw')
        plti.plot(self.time,self.truncated_bits,label='Truncated')
        plti.plot(self.time,self.filtered_bits,label='Filtered')
        plti.legend()
        pp.savefig()

    def plot_windspeed(self,pp):
        if self.WIND != None:
            title = 'Average Wind Speed for Run = ' + str(np.round(self.WIND,2)) + ' m/s'
        else:
            title = 'Pitot Probe File = '+self.fileName
        plti = P.plottool(12,'Time (sec)','WindSpeed (m/s)',title)
        plti.plot(self.time,self.airspeed_ms,label='Raw')
        plti.plot(self.time,self.airspeed_ms_filtered,label='Filtered')
        plti.legend()
        pp.savefig()

    def plot_raw_bits(self,pp):
        plti = P.plottool(12,'Time (sec)','Pitot Raw Bits','Pitot Probe File = '+self.fileName)
        plti.plot(self.time,self.raw_bits)
        pp.savefig()

    def convert_pitot(self,bit_threshold,wc,sigma,*therest):
        #The variable therest is a wildcard and should contain the PTH data. you can see what is in that data list by calling
        #print data_PTH[-1]
        ambient_pressure_kpa = []
        if len(therest) > 0:
            data_PTH = therest[0]
            #print data_PTH[-1]
            temperature_C = data_PTH[1]
            ambient_pressure_kpa = data_PTH[2]/10.0
            #print ambient_pressure_kpa
        else:
            temperature_C = []

        #Need to get the average no wind bits
        #Assume you at least have 100 data points
        if len(self.raw_bits) > 100:
            average_bits = np.mean(self.raw_bits[0:100])
            print 'Average Bits = ',average_bits
        else:
            average_bits = self.raw_bits[0]

        ##Let's convert average bits to meanV
        #average_bits = (1023.0/5.0)*meanV
        meanV = (5.0/1023.0)*average_bits
    
        ##One thing I realized is that when the sensor picks up a change
        ##in bit say from 520 to 521 bits this is really just signal
        #noise. I've run the sensor literally just sitting there on the
        #ground and the bit flips from a stock value to plus or minus 1. I
        #think we need to "filter" this out. Another reason for this is
        #because when a bit flips by 1 just 1 the change in m/s is 3
        #m/s. That's insane. That means our signal noise accounts for 3
        #m/s!!! A larger change in bits results in a much smaller change
        #per bit so we definitely want to get rid of this plus or minus 1
        #BS. Honestly we may want to consider plus or minus 2.

        #Alright. So since we don't want to truncate K at 0 let's filter x
        #before we march along
        #One thing that might make more sense is to run an actual low pass
        #filter rather than this really bad complimentary filter
        self.truncated_bits = np.copy(self.raw_bits)
        for x in range(0,len(self.raw_bits)):
            if np.abs(self.raw_bits[x] - average_bits) <= bit_threshold:
                self.truncated_bits[x] = average_bits

        indices = self.truncated_bits < average_bits
        self.truncated_bits[indices] = average_bits

        if wc != -99:
            [self.filtered_bits,self.filtered_time] = LowPass(self.truncated_bits,self.time,wc)
        else:
            self.filtered_bits = np.copy(self.truncated_bits)
            # filtered_bits = np.zeros(len(raw_bits))
        # filtered_bits[0] = raw_bits[0]
        # for idx in range(0,len(raw_bits)-1):
        #     filtered_bits[idx+1] = (1-sigma)*filtered_bits[idx] + sigma*raw_bits[idx]

        #Ok so other problem. Remember the plots are most sensitive when
        #the delta bits is small. So....it means we need to truncate the
        #bits again after we filter
        # filtered_truncated_bits = deepcopy(filtered_bits)
        # for x in range(0,len(raw_bits)):
        #     if np.abs(filtered_bits[x] - average_bits) <= 2:
        #         filtered_truncated_bits[x] = average_bits
        
        #The question now is what do we want to use to filter this signal?
        self.voltage = self.filtered_bits*(5.0/1023.0); 

        self.pressure_kpa = (self.voltage-meanV);

        ##I think this is actually just a standard unit conversion from kpa to atm
        self.pressure_atm = self.pressure_kpa/101.325;

        ##We need to make sure pressure_atm > -1.0
        for x in range(0,len(self.pressure_atm)):
            if self.pressure_atm[x] < -1.0:
                self.pressure_atm[x] = -1.0

        ####This equation here comes from bernoulli
        self.k = 5*((self.pressure_atm+1.0)**(2.0/7.0)-1.0);
        
        #There is a potential here for
        #k to be less than 0. If that happens, the sqrt goes imaginary
        #Thus we need to add in a fix here
        #So the issue with truncating k at 0 is that when we filter. We
        #loose half of the information. So really what we need to do is
        #filter the bits before we run them through everything
        indices = self.k < 0.0
        self.k[indices] = 0.0

        #This is the rest of the equation from bernoulli. 343.2 is the speed of
        #REVISIT REVISIT
        #sound at sea-level
        #Sqrt(gamma*R*T) - Replace with this!
        #T is in Kelvin
        #R is 286 ideal gas constant
        #Gamma is the adiabatic index = 1.4
        if len(temperature_C) == 0:
            temperature_C = 20*np.ones(len(self.k))

        tempK = temperature_C + 273.15
        a_inf = np.sqrt(1.4*286*tempK)
        self.airspeed_ms = a_inf*self.k**(0.5)

        #Ok here's where we need to zero out everything before cal_start
        # for x in range(0,len(airspeed_ms)):
        #     if time_in[x] < cal_end:
        #         #print "Zeroing..."
        #         airspeed_ms[x] = 0.0

        #Because the initial voltage is used as the tare we can zero 
        #out the windspeed here. We can't zero out the voltage because of raising
        #k to 1/2 power. k must be positive so we can't have negative voltage
        #so we have to tare here.
        # t = tot_time_sec_zero[0]
        # print "INITIAL T = ",t,"GPS_ACQUIRED_SECONDS = ",GPS_ACQUIRED_SECONDS
        # meanU = 0;
        # numData = 0;
        # for t in tot_time_sec_zero:            
        #     if t >= CAL_START and t <= CAL_END:
        #         meanU += airspeed_ms[numData]
        #         numData += 1
        # if numData == 0:
        #     numData = 1
        
        # print 'meanU = ',meanU/numData
        # airspeed_ms = airspeed_ms-meanU/numData

        #print('Filtering Signal...')
        
        ##Run signal through a complimentary filter
        #sigma = 0.03 #Made this an input to the function so we can change it on the fly
        self.airspeed_ms_filtered = Complimentary(sigma,self.airspeed_ms)

    def get_single_data_point(self):
        #Assume that self.airspeed_ms exists
        #Only find the data points with data
        indices = self.airspeed_ms > 0.0
        if len(indices) > 0:
            self.WIND = np.mean(self.airspeed_ms[indices])
        else:
            self.WIND = 0.0
