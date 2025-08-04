#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
from gps import *
from pdf import *
#from fileinput import filename

if __name__ == "__main__":
    
    plt.close("all")
    
    plt.rcParams.update({'font.size':18})

    raw_bits = np.linspace(521,531,100)
    average_bits = 520
    meanV = 520*(5.0/1023.0)
    voltage = raw_bits*(5.0/1023.0); 
    pressure_kpa = voltage-meanV;
    pressure_atm = pressure_kpa/101.325;
    k = 5*((pressure_atm+1.0)**(2.0/7.0)-1.0);
    tempC = 20
    tempK = tempC + 273.15
    a_inf = np.sqrt(1.4*286*tempK)
    airspeed_ms = a_inf*k**(0.5)
    #print "Raw_Bits = ",raw_bits
    #print "Airspeed (m/s) = ",airspeed_ms
    delta_bits = (raw_bits-average_bits)
    sensitivity = airspeed_ms/delta_bits
    print "Sensitivity (m/s per bit) = ",sensitivity
    #pp = PDF(0,plt)
    plt.figure()
    plt.plot(delta_bits,sensitivity)
    plt.xlabel('Change in Bits')
    plt.ylabel('Sensitivity (m/s per bit)')
    plt.grid()
    #pp.savefig()
    #pp.close()
    
    plt.figure()
    plt.plot(delta_bits,airspeed_ms)
    plt.xlabel('Change in Bits')
    plt.ylabel('Airspeed (m/s)')
    plt.grid()
    
    plt.show()
