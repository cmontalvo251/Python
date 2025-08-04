#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys
import csv
from gps import *
from pdf import *
from copy import deepcopy
from mymath import LowPass
#from fileinput import filename

##The Pitot probes are plugged into the Arduino in this order. Thus when reading the SD
#card you need to make sure you place everything in the correct slot.
#remember that these are the Quadcopter reference frames. If you fly the quad in a different direction
#everything will get rotated. Honestly I recommend flying in the direction of cardinal north to avoid any sort of confusion
PitotName = ['North','East','West','South']

def get_pitot_simple(inputfilename,numPitots):
    #Read data from file
    print('Loading Pitot Probe File...',inputfilename)

    time_arduino = []
    raw_pitot = []

    pitotdata = open(inputfilename)

    print('Pitot File = ',numPitots)

    for line in pitotdata:
        #and pitot probe data
        row = line.split(' ')
        #print row
        time_arduino.append(row[0])
        pitots = []
        for x in range(0,numPitots):
            pitots.append(np.float(row[x+1]))
        raw_pitot.append(pitots)
        
    raw_np = np.array(raw_pitot)

    return [[],[time_arduino,[],[],raw_np]]

def get_pitot_data(inputfilename,numPitots,sigma,CAL_TIMES,*therest):
    #Read data from file
    print('Loading Pitot Probe File...',inputfilename)
    
    #Therest is a wildcard set of variables which may or may not be passed to this function
    #debugmode=0,pp=None,NOPGS=None
    if len(therest) > 0:
        debugmode = therest[0]
    else:
        debugmode = 0
    if len(therest) > 1:
        pp = therest[1]
    else:
        pp = None
    if len(therest) > 2:
        NOGPS = therest[2]
    else:
        NOGPS = 0

    try:
        pitotdata = open(inputfilename)
    except:
        pitotdata = None

    if pitotdata == None:
        print('Sorry. File: ',inputfilename,' could not be found')
        return 0

    time_arduino = []
    gps_data = []
    raw_pitot = []
    lat_vec = []
    lon_vec = []
    temp_vec = []
    pressure_vec = []
    humidity_vec = []
    time_gps = []
    alt_vec = []
    alt_old = 0
    time_hr = -1
    arduino_roll_over = 0
    totalBits = np.zeros([4,1])
    numData_Bits = 0.0
    DONE_CALIBRATE = False
    GPS_ACQUIRED_SECONDS = 0
    CAL_TIME = 20 #if GPS is never acquired we will use the first 20 seconds

    CAL_START = CAL_TIMES[0]
    if CAL_START == -99 or NOGPS:
        CAL_START = 0
        CAL_END = CAL_TIME
    else:
        CAL_END = CAL_TIMES[1]
        
    print('CAL_TIMES = ',CAL_START,CAL_END)
        
    # gps_data needs to be like this
    # lat_vec_np = data[0]
    # lon_vec_np = data[1]
    # time_vec_np = data[2]
    # x_vec_np = data[3]
    # y_vec_np = data[4]
    # alt_vec_np = data[5]
    
    lenfile = 0

    for line in pitotdata:
        lenfile+=1
        #Make sure the length of the row is valid
        if len(line) > 2:
            row = line.split(' ')
            
            ####I'm going to calibrate the voltage here
            #I think I'm going to have to set these calibration gates myself
            arduino_time = np.float(row[1])
            if arduino_time >= CAL_START and arduino_time <= CAL_END:
                numData_Bits+=1.0
                #print numData_Bits
                for pitoti in range(0,numPitots):
                    totalBits[pitoti] += np.float(row[7+pitoti])

            #Need to add one more check for time
            time_split = row[0].split(':')
            #If the hour is zero and time_hr hasn't been initialized 
            #This makes sure that the time is not zero, you haven't initialized time_hr
            #and you have a valid GPS loc. This should only run once
            if (np.float(time_split[0]) != 0 and time_hr == -1):
                if abs(np.float(row[2])) > 28 and abs(np.float(row[2])) < 32:
                    if abs(np.float(row[3])) > 86 and abs(np.float(row[3])) < 90:
                        if abs(np.float(row[6])) < 1000 and abs(np.float(row[6]))>10:
                            #Otherwise save the current time
                            time_hr = np.float(time_split[0])
                            time_new = NMEA_TIME(row[0],'hrs')
                            #Save Previous values of lat lon and altitude
                            lat_new = np.float(row[2])
                            lon_new = np.float(row[3])
                            alt_new = np.float(row[6])
                            print("Hour of Day = ",time_hr)
                            print("GPS Coordinate = ",lat_new," ",lon_new)
                            print("Altitude = ",alt_new)
                            GPS_ACQUIRED_SECONDS = arduino_time
                            print('GPS ACQUIRED AT SEC = ',GPS_ACQUIRED_SECONDS)

            #Don't grab data until we have a GPS loc
            #The above line of code makes sure we don't grab any data until we have a loc. 
            #Technically this is just as bad as the iMet but this line of code actually just says
            #once you get a lock. Take data. Furthermore the sensor itself is always sensing data we just aren't plotting
            #data until we get a lock. The lines that follow check to make sure we have a lock. If we don't it might mean we just 
            #lost the loc so we will just assume that the previous data point is valid

            #Problem is what if we never get a lock. What if we're doing an experiment in the lab and
            #we just want to plot some data and see what's going on?
            if NOGPS:
                time_new = 0
                time_hr = 0
                lat_new = 0
                lon_new = 0
                alt_new = 0

            #If this is tru it means we had a GPS loc at one point or another
            if time_hr != -1 or NOGPS:
                #Check and make sure our time is valid otherwise use previous value?
                if abs(NMEA_TIME(row[0],'hrs')-time_new) < 1:
                    time_new = NMEA_TIME(row[0],'hrs')
                time_gps.append(time_new)
                #print time_new

                #Check and see if our GPS Latitude is valid
                if abs(np.float(row[2])) > 28 and abs(np.float(row[2])) < 32: 
                    #We still have a GPS loc so update the value
                    lat_new = np.float(row[2])
                lat_vec.append(lat_new)

                #Check and see if our GPS longitude is valid
                if np.float(row[3]) > -90 and np.float(row[3]) < -86: 
                    #We still have a GPS loc so update the value
                    lon_new = np.float(row[3])
                lon_vec.append(lon_new)

                #Check and see if our altitude is still valid (Needed to add > 10 to fix some GPS dropouts from PTH sensor)
                if np.float(row[6]) > 10 and np.float(row[6]) < 1000:
                    if len(alt_vec)>0:
                        if abs(np.float(row[6])-alt_vec[-1]) < 80:
                            alt_new = np.float(row[6])
                    else:
                        alt_new = np.float(row[6])
                alt_vec.append(alt_new)

                #Get Temperature/Pressure/Humidity if the data allows
                if len(row) > 7+numPitots+4:
                    temp = np.float(row[11])
                    pressure = np.float(row[12])
                    humidity = np.float(row[13])
                    temp_vec.append(temp)
                    pressure_vec.append(pressure)
                    humidity_vec.append(humidity)

                #Always append arduino time
                #we need to save a roll over since some files are separate. This is pre-11_29_2016 or somewhere around there.
                try:
                    if np.float(row[1])+arduino_roll_over < time_arduino[-1]:
                        arduino_roll_over = time_arduino[-1]
                except:
                    print("Skipping First Data point for roll over")
                time_arduino.append(np.float(row[1])+arduino_roll_over)

                #and pitot probe data
                pitots = []
                for x in range(0,numPitots):
                    raw_bits = np.float(row[7+x])
                    #if time_arduino[-1] < CAL_START:
                    #    raw_bits = -99 #It's possible to calibrate after you've acquired GPS
                        #in this case we will put a -99 as a place holder and fix this later
                    pitots.append(raw_bits)
                    #print pitots
                raw_pitot.append(pitots)

    print('File Loaded')

    #At this point it is possible to compute averagebits and replace all the -99's with
    #just the average bit number
    # I don't like this. Because this destroys all the raw bit
    #information. I'd rather do this during the conversion
    #process. Problem is that means we have to send CAL TIMES to
    #convert_pitot or send some sort of marker that says everything
    #before this position should be zero. 
    # for x in range(0,len(raw_pitot)):
    #     for p in range(0,numPitots):
    #         if raw_pitot[x][p] == -99:
    #             raw_pitot[x][p] = totalBits[p]/numData_Bits

    #In other news it turns out that fastwing.py uses convert_pitot()
    #which means we're going to have to handle everything in that
    #function. So yea we're going to have to send a var that indicates
    #when to truncate.

    #Convert everything to np lists
    lat_vec_np = np.array(lat_vec)
    lon_vec_np = np.array(lon_vec)
    time_gps_np = np.array(time_gps)
    alt_vec_np = np.array(alt_vec)

    #Get arduino and gps delta
    if len(time_gps_np) > 0:
        dt_gps = (time_gps_np[-1] - time_gps_np[0])*3600 #Assume gps is in seconds
        dt_arduino = time_arduino[-1] - time_arduino[0]
    else:
        print("Sorry, GPS never acquired. Replotting code with NO GPS")
        data_pitot = get_pitot_data(inputfilename,numPitots,sigma,CAL_TIMES,debugmode,pp,1)
        return data_pitot

    #Now we must scale the arduino time to match gps_time

    #Set pitot probe time to arduino time for now
    time_np = np.array(time_arduino)
    #Offset arduino timer by the GPS timer but only do this if we actually had GPS
    if NOGPS == 0:
        time_np = (time_np-time_np[0])*dt_gps/dt_arduino
    raw_np = np.array(raw_pitot)

    #Now recheck the arduino time_np
    #dt_arduino_new = time_np[-1]-time_np[0]
    #print dt_gps,dt_arduino,dt_arduino_new

    #With the pitot time shifted it's possible now to compute total gps+arduino time
    time_arduino_hr = time_np/3600
    time_arduino_hr_offset_gps = time_arduino_hr + time_gps_np[0]
    tot_time = []
    gps_offset = 0
    tot_time1 = time_gps_np[0]
    gps_old = time_gps_np[0]
    lastGPStime = 0

    for x in range(0,len(time_gps_np)):
        #Reset Arduino clock
        if time_gps_np[x] != gps_old:
            lastGPStime = time_arduino_hr[x]
            gps_old = time_gps_np[x]

        new_time = time_gps_np[x] + time_arduino_hr[x] - lastGPStime
 
        if len(tot_time) > 0:
            if new_time <= tot_time[-1]:
                lastGPStime = lastGPStime - tot_time[-1] + new_time
                new_time = time_gps_np[x] + time_arduino_hr[x] - lastGPStime
                #Double check for multiple times
                if new_time == tot_time[-1]:
                    new_time = new_time + 1e-8
            
        tot_time.append(new_time)

    tot_time_np = np.array(tot_time)

    tot_time_hr = tot_time_np
    tot_time_sec = tot_time_np*3600
    tot_time_sec_zero = tot_time_sec - tot_time_sec[0]

    print("GPS TIME SET")

    if NOGPS:
        tot_time_sec_zero = time_np #If we never got GPS and we are just doing an experiment in the lab
        #just use the arduino timer
        #print time_np

    del_min = np.ceil((time_gps_np[-1]-time_gps_np[0])*60.0/10.0) #number of minutes
    print("DEL_MIN = ",del_min)
    time_vec_HHMM,xticks = HHMM_Format(time_gps_np,del_min)

    print("XTICKS CREATED")

    if debugmode == 1:
        plt.figure()
        plt.plot(time_gps_np,color='blue',label="GPS Time")
        plt.plot(time_arduino_hr_offset_gps,color='red',label="Scaled Arduino + GPS Offset Time")
        plt.plot(tot_time_np,color='green',label="GPS+Arduino Time")
        plt.xlabel('Row Number')
        plt.ylabel('Time (hrs)')
        plt.legend(loc=2)
        plt.grid()
        pp.savefig()

        print("FIG 1")

        plt.figure()
        for pitoti in range(0,numPitots):
            plt.plot(tot_time_sec_zero+GPS_ACQUIRED_SECONDS,raw_np[:,pitoti],label=PitotName[pitoti])
        plt.xlabel('Time (sec)')
        plt.ylabel('Raw Bits (0-1023) Sensor')
        plt.legend(loc='best')
        plt.grid()
        #plt.xlim([400,800])
        #plt.ylim([505,535])
        pp.savefig()

        print("FIG 2")

        if del_min != 0:
            figureRAW = plt.figure()
            pltRAW = figureRAW.add_subplot(1,1,1)
            for pitoti in range(0,numPitots):
                pltRAW.plot(time_gps_np,raw_np[:,pitoti],label=PitotName[pitoti])
            pltRAW.set_xlabel('Time (HH:MM)')
            pltRAW.set_ylabel('Raw Bits (0-1023) Sensor')
            plt.legend(loc='best')
            pltRAW.set_xticks(xticks) #linspace - start,end,number of points
            pltRAW.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
            pltRAW.grid()
            pp.savefig()

    print("FIGURES CREATED")

    #Convert lat and lon to Cartesian Coordinates
    if len(lat_vec_np) > 1:
        origin = [lat_vec_np[0],lon_vec_np[0]]
    else:
        origin = [0,0]

    lat_lon = [lat_vec_np,lon_vec_np]
    xy = convertLATLON(lat_lon,origin)
    x_vec_np = xy[0]
    y_vec_np = xy[1]

    airspeed_ms_filtered_all = []
    airspeed_ms_all = []

    #print raw_np[0,:] #- this is the entire first data point of all pitot probes
    #print raw_np[:,0] #- this is the first pitot probe

    #Convert Pressure to Altitude
    pressure_np = np.array(pressure_vec)
    if len(pressure_np) > 0:
        pressure_altitude_np = 44330.0 * (1.0 - pow(pressure_np/pressure_vec[0], 0.1903));
    else:
        pressure_altitude_np = []
        
    ###Temperature/Pressure/Humidity
    PTH_directory = "Temperature/Pressure/Humidity \n" + "tot_time_sec_zero - 0 \n" + "Temperature (C) - 1 \n" + "Pressure (hPa) - 2 \n" + "Humidity (%) - 3 \n" + "Pressure Altitude (m) - 4 \n"
    PTH_data = [tot_time_sec_zero,np.array(temp_vec),pressure_np,np.array(humidity_vec),pressure_altitude_np,PTH_directory]

    ###LET"S HARDCODE A SCALE FACTOR AT THE MOMENT
    SCALE = [1,1,1,1]

    ###CONVERT RAW SIGNAL TO VOLTS - The raw signal is a 10-bit register
    ###so you need to convert it to volts. 2^10 = 1024 so basically 1024 =
    ###5 volts - it's completely linear
    for pitoti in range(0,numPitots):
        print('Total Bits = ',totalBits[pitoti])
        print('Num Data = ',numData_Bits)
        averageBits = totalBits[pitoti]/(numData_Bits)
        print('Average Bits = ',averageBits)
        ##Calculate meanV based on total bits
        meanV = (5.0/1023.0)*averageBits
        print('Calibrated Voltage = ',meanV)
        [airspeed_ms_filtered,airspeed_ms] = convert_pitot(tot_time_sec_zero+GPS_ACQUIRED_SECONDS,CAL_END,raw_np[:,pitoti],meanV,sigma,pitoti,debugmode,pp,PTH_data)

        ####ADD A SCALE FACTOR NOT SURE WHAT TO DO ABOUT DETERMINING THIS VALUE BUT I"LL CODE IT IN FOR THE MOMENT
        airspeed_ms = SCALE[pitoti]*airspeed_ms
        airspeed_ms_filtered = SCALE[pitoti]*airspeed_ms_filtered
    
        airspeed_ms_filtered_all.append(airspeed_ms_filtered)
        airspeed_ms_all.append(airspeed_ms)

    #Return Data
    # gps_data needs to be like this
    # lat_vec_np = data[0]
    # lon_vec_np = data[1]
    # time_vec_np = data[2]
    # x_vec_np = data[3]
    # y_vec_np = data[4]
    # alt_vec_np = data[5]
    directory_gps = "GPS Data \n" + "Latitude - 0 \n" + "Longitude - 1 \n" + "tot_time_hr - 2 \n" + "x_vec_np - 3 \n" + "y_vec_np - 4 \n" + "alt_vec_np - 5 \n" + "Note that GPS Start = data[2][0] and GPS End = data[2][-1] \n"
    data_gps = [lat_vec_np,lon_vec_np,tot_time_hr,x_vec_np,y_vec_np,alt_vec_np,directory_gps]
    # It seems like our pitot data is off by 1 minute. Seems reasonable.
    # Pitot data is like this
    # tot_time_sec_zero = data[0]
    # airspeed_ms_filtered_all = data[1]
    # airspeed_ms_all = data[2]
    directory_pitot = "Pitot Data \n" + "tot_time_sec_zero - 0 \n" + "airspeed_ms_filtered_all - 1 \n" + "airspeed_ms_all - 2 \n" + "raw_data - 3 \n" + "numpitot = len(airspeed_ms_all) \n" + "Pitot Orientation = West,North,South,East (Qaud Ref) \n"
    data_pitot = [tot_time_sec_zero,airspeed_ms_filtered_all,airspeed_ms_all,raw_np,directory_pitot]
    
    #Create a directory of everything
    directory_all = "FASTPitot Sensor Data \n" + "GPS Data - 0 \n" + "Pitot Data - 1 \n" + "Temperature/Pressure/Humidity Data - 2 \n"

    #Combine into data ball
    data = [data_gps,data_pitot,PTH_data,directory_all]

    return data

def create_pitot_plots(data_pitot,numPitots,pp):
    #Create Pitot Plots
    tot_time_sec_zero = data_pitot[0]
    airspeed_ms_filtered_all = data_pitot[1]
    airspeed_ms_all = data_pitot[2]

    ##PROCESSED DATA
    plt.figure()
    mycolors = ['blue','purple','green','cyan']

    print tot_time_sec_zero[0],tot_time_sec_zero[-1]
    
    for x in range(0,numPitots):
        #plt.plot(time_truth,speed_truth)
        #plt.plot(tot_time_sec_zero,airspeed_ms_all[x],color='green')
        plt.plot(tot_time_sec_zero,airspeed_ms_filtered_all[x],color=mycolors[x],label=PitotName[x])
    plt.xlabel('Time (sec)')
    plt.ylabel('Windspeed (m/s)')
    plt.xlim([tot_time_sec_zero[0],tot_time_sec_zero[-1]])
    plt.legend(loc='best')
    plt.grid()
    pp.savefig()

def create_PTH_plots(data_PTH_all,data_gps_all,pp):
    #data_PTH_all is multiple data streams up to two
    f = plt.figure()
    p = f.add_subplot(1,1,1)

    #TEMPERATURE
    for x in range(0,len(data_PTH_all)):
        data_PTH = data_PTH_all[x]
        #Create PTH Plots
        tot_time_sec_zero = data_PTH[0]
        temperature = data_PTH[1]
        pressure = data_PTH[2]
        humidity = data_PTH[3]
        pressure_altitude = data_PTH[4]
    
        ##PROCESSED DATA
        if len(temperature) > 0:
            p.plot(tot_time_sec_zero,temperature)
            
    p.set_xlabel('Time (sec)')
    p.set_ylabel('Temperature (C)')
    p.grid()
    p.get_yaxis().get_major_formatter().set_useOffset(False)
    pp.savefig()

    #PRESSURE
    f2 = plt.figure()
    p2 = f2.add_subplot(1,1,1)

    for x in range(0,len(data_PTH_all)):
        data_PTH = data_PTH_all[x]
        #Create PTH Plots
        tot_time_sec_zero = data_PTH[0]
        temperature = data_PTH[1]
        pressure = data_PTH[2]
        humidity = data_PTH[3]
        pressure_altitude = data_PTH[4]
    
        ##PROCESSED DATA
        if len(pressure) > 0:
            p2.plot(tot_time_sec_zero,pressure)
            
    p2.set_xlabel('Time (sec)')
    p2.set_ylabel('Pressure (hPa)')
    p2.grid()
    p2.get_yaxis().get_major_formatter().set_useOffset(False)
    pp.savefig()
    
    #HUMIDITY
    plt.figure()
    for x in range(0,len(data_PTH_all)):
        data_PTH = data_PTH_all[x]
        #Create PTH Plots
        tot_time_sec_zero = data_PTH[0]
        temperature = data_PTH[1]
        pressure = data_PTH[2]
        humidity = data_PTH[3]
        pressure_altitude = data_PTH[4]

        if len(humidity) > 0:
            plt.plot(tot_time_sec_zero,humidity)
    plt.xlabel('Time (sec)')
    plt.ylabel('Humidity (%)')
    plt.grid()
    pp.savefig()

    #PRESSURE ALTITUDE
    plt.figure()
    for x in range(0,len(data_PTH_all)):
        data_PTH = data_PTH_all[x]
        data_gps = data_gps_all[x]
        #Create PTH Plots
        tot_time_sec_zero = data_PTH[0]
        temperature = data_PTH[1]
        pressure = data_PTH[2]
        humidity = data_PTH[3]
        pressure_altitude = data_PTH[4]
        if len(pressure_altitude) > 0:
            plt.plot(tot_time_sec_zero,pressure_altitude,label='Pressure')

            #3/31/2017 - FP4H
            #times = [120,210,380,500]
            #3/31/2017 - FP4V
            times = [160,280,450,575]
            
            loc = np.where(tot_time_sec_zero < times[0])
            first_ascent = loc[0][-1]
            loc = np.where(tot_time_sec_zero < times[1])
            first_peak = loc[0][-1]
            loc = np.where(tot_time_sec_zero < times[2])
            second_ascent = loc[0][-1]
            loc = np.where(tot_time_sec_zero < times[3])
            second_peak = loc[0][-1]
            
            plt.plot(tot_time_sec_zero[first_ascent],pressure_altitude[first_ascent],'g*')

            plt.plot(tot_time_sec_zero[first_peak],pressure_altitude[first_peak],'r*')

            plt.plot(tot_time_sec_zero[second_ascent],pressure_altitude[second_ascent],'gs')
            
            plt.plot(tot_time_sec_zero[second_peak],pressure_altitude[second_peak],'rs')
            
            plt.plot(tot_time_sec_zero,data_gps[5],label='GPS')
            alt_offset = 0
            for alt in data_gps[5]:
                if alt_offset == 0 and alt != 0:
                    alt_offset = alt
            plt.plot(tot_time_sec_zero,pressure_altitude+alt,label='Pressure+GPS Offset')
    plt.xlabel('Time (sec)')
    plt.ylabel('Altitude (m)')
    plt.grid()
    plt.legend()
    pp.savefig()

    PTH_PITOT = 1

    figureALT_Temp = plt.figure()
    pltALT_Temp = figureALT_Temp.add_subplot(1,1,1)
    pltALT_Temp.plot(temperature,pressure_altitude,label='FASTPitot')

    pltALT_Temp.plot(temperature[first_ascent],pressure_altitude[first_ascent],'g*')
    pltALT_Temp.plot(temperature[first_peak],pressure_altitude[first_peak],'r*')
    pltALT_Temp.plot(temperature[second_ascent],pressure_altitude[second_ascent],'gs')
    pltALT_Temp.plot(temperature[second_peak],pressure_altitude[second_peak],'rs')
    
    ###Labeling and Stuff
    pltALT_Temp.set_xlabel('Temperature (C)')
    pltALT_Temp.set_ylabel('Pressure Altitude (m)')
    pltALT_Temp.legend(loc='best')
    pltALT_Temp.grid()
    pp.savefig()
    print 'Plotting Temp vs Alt'

    figureALT_Press = plt.figure()
    pltALT_Press = figureALT_Press.add_subplot(1,1,1)

    pltALT_Press.plot(pressure,data_gps[5],label='FASTPitot')

    pltALT_Press.plot(pressure[first_ascent],data_gps[5][first_ascent],'g*')
    pltALT_Press.plot(pressure[first_peak],data_gps[5][first_peak],'r*')
    pltALT_Press.plot(pressure[second_ascent],data_gps[5][second_ascent],'gs')
    pltALT_Press.plot(pressure[second_peak],data_gps[5][second_peak],'rs')

    ##Labeling and Stuff
    pltALT_Press.set_xlabel('Pressure (kPa)')
    pltALT_Press.set_ylabel('GPS Altitude (m)')
    pltALT_Press.get_xaxis().get_major_formatter().set_useOffset(False)
    pltALT_Press.legend(loc='best')
    pltALT_Press.grid()
    pp.savefig()
    print 'Plotting Pressure vs Alt'

    figureALT_Hum = plt.figure()
    pltALT_Hum = figureALT_Hum.add_subplot(1,1,1)
    pltALT_Hum.plot(humidity,pressure_altitude,label='FASTPitot')

    pltALT_Hum.plot(humidity[first_ascent],pressure_altitude[first_ascent],'g*')
    pltALT_Hum.plot(humidity[first_peak],pressure_altitude[first_peak],'r*')
    pltALT_Hum.plot(humidity[second_ascent],pressure_altitude[second_ascent],'gs')
    pltALT_Hum.plot(humidity[second_peak],pressure_altitude[second_peak],'rs')
    
    ###Labeling and Stuff
    pltALT_Hum.set_xlabel('Relative Humidity (%)')
    pltALT_Hum.set_ylabel('Pressure Altitude (m)')
    pltALT_Hum.legend(loc='best')
    pltALT_Hum.grid()
    pp.savefig()
    print 'Plotting Humidity vs Alt'

def create_text_file(data,fileoutname):
    #Now we need to output all the data to a text file for MATLAB use
    # GPS+Arduino time in hours - 1
    # Latitude - 2
    # Longitude - 3
    # Altitude (for quad output the autopilot altitude, for pitot output the the pressure altitude offset by GPS?) - 4
    # Phi - for pitot just output all zeros for this - 5
    # Theta - 6
    # Psi - 7
    # Lateral speed - for pitot just output GPS.speed - 8
    # Lateral speed- 9 - crap. GPS.speed got commented out because of space issues
    # Vertical speed - fp4 all -99 - 10
    # P - pitot all -99 - 11
    # Q - 12
    # R - 13
    # Ax - pitot all -99 - 14
    # Ay - 15
    # Az - 16
    # A0 - for quad all -99 - 17
    # A1 - 18
    # A2 - raw bits for pitot probe so we can use Matlab to calibrate - 19
    # A3 - 20
    # Temperature - all -99 for quad - 21
    # Pressure - 22 - except for this one
    # Humidity - 23
    # print data[-1]
    gps_data = data[0]
    pitot_data = data[1]
    pth_data = data[2]
    # print gps_data[-1]
    # print pitot_data[-1]
    # print pth_data[-1]

    tot_time_hr = gps_data[2]

    #Calibrate ALtitude
    pressure_altitude = pth_data[4]
    if len(pressure_altitude) > 0:
        altitude = pressure_altitude + gps_data[5][0]
    else:
        altitude = gps_data[5]

    raw_pitot = pitot_data[3]
    airspeed_ms_all = pitot_data[2]
    airspeed_ms_filtered_all = pitot_data[1]

    csvwriter = csv.writer(open(fileoutname,"wb"),delimiter=",")

    temperature = pth_data[1]
    pressure = pth_data[2]
    humidity = pth_data[3]
    if len(temperature) == 0:
        temperature = -99*np.ones(len(altitude))
        pressure = temperature
        humidity = pressure

    print('All these numbers should be the same = ',len(gps_data[0]),len(temperature),len(raw_pitot[:,0]))
        
    for idx in range(0,len(tot_time_hr)):
        # GPS Data
        # tot_time_hr - 2        
        row = [tot_time_hr[idx],
        # Latitude - 0
               gps_data[0][idx],
        # Longitude - 1
               gps_data[1][idx],
        # x_vec_np - 3 
        # y_vec_np - 4 
        # alt_vec_np - 5
               altitude[idx],
        # Note that GPS Start = data[2][0] and GPS End = data[2][-1]
        # Phi,theta,psi
               -99,
               -99,
               -99,
        # ,xdot,ydot,zdot
               -99,
               -99,
               -99,
        # p,q,r
               -99,
               -99,
               -99,
        # Ax,Ay,Az
               -99,
               -99,
               -99,
        # Pitot Data 
        # tot_time_sec_zero - 0 
        # airspeed_ms_filtered_all - 1 
        # airspeed_ms_all - 2 
        # raw_data - 3
               raw_pitot[idx,0],
               raw_pitot[idx,1],
               raw_pitot[idx,2],
               raw_pitot[idx,3],
        # print row
        # numpitot = len(airspeed_ms_all) 
        # Pitot Orientation = West,North,South,East (Qaud Ref) 
    
        # Temperature/Pressure/Humidity 
        # tot_time_sec_zero - 0
        # Temperature (C) - 1
               temperature[idx],
        # Pressure (hPa) - 2 - CONVERTED TO KPA
               pressure[idx]*0.1,
        # Humidity (%) - 3
               humidity[idx],
        # Airspeed data
               airspeed_ms_filtered_all[0][idx],
               airspeed_ms_filtered_all[1][idx],
               airspeed_ms_filtered_all[2][idx],
               airspeed_ms_filtered_all[3][idx],
        ]
        # Pressure Altitude (m) - 4
        csvwriter.writerow(row)

    print("Logfile written to "+fileoutname)


def convert_pitot(time_in,cal_end,raw_bits,meanV,sigma,pitoti,debugmode,pp,*therest):
    #The variable the rest is a wildcard and should contain the PTH data. you can see what is in that data list by calling
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

    
    ##Let's convert meanV back to average_bits so we can use it for
    ##some filtering
    average_bits = (1023.0/5.0)*meanV
    
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
    truncated_bits = deepcopy(raw_bits)
    for x in range(0,len(raw_bits)):
        if np.abs(raw_bits[x] - average_bits) <= 1.5:
            truncated_bits[x] = average_bits
    
    wc = 0.25 #what about 0.25*2*np.pi? That would be 0.25 Hz as suggested by FFT from 11/15/2017 quad flights. :/
    #wc = 100.0
    [filtered_bits,filtered_time] = LowPass(truncated_bits,time_in,wc)
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
    voltage = filtered_bits*(5.0/1023.0); 

    ##################THIS CALIBRATION HAS MOVED TO THE IMPORT ROUTINE#########################

    #//2.5 volts should equal zero kPa. Should probably just calibrate
    #this every time instead of storing a random number
    #Apprarently this gives pressure in kPa which means the voltage is a
    #function of pressure
    #This is a main source of error here. I think we need to compute this earlier
    #t = tot_time_sec_zero[0]
    #meanV = 0;
    #numData = 0;
    #time_avg = 20 ##NEED TO MESS WITH THIS. I THINK THE IS THE ISSUE RIGHT HERE
    #while t < time_avg:
    #    meanV += voltage[numData]
    #    numData += 1
    #    t = tot_time_sec_zero[numData]
    
    #if numData == 0:
    #    numData = 1
    #meanV = meanV/numData
    #meanV = 0
    #meanV = min(voltage)
    
    #We need to substract off like the first 5 seconds of data instead of
    #using just a saved number
    
    ##########################################################################################
    pressure_kpa = (voltage-meanV);

    #This is actually what we want.
    #OR IS IT REALLY? I DON"T ACTUALLY KNOW. Bleh.
    #if len(ambient_pressure_kpa) > 0:
        #print (ambient_pressure_kpa-ambient_pressure_kpa[0])
        #pressure_kpa = pressure_kpa - (ambient_pressure_kpa-ambient_pressure_kpa[0])
        
    ###Zero out erroneous signals
    # if CAL_START > GPS_ACQUIRED_SECONDS:
    #     for x in range(0,len(pressure_kpa)):
    #         if tot_time_sec_zero[x] <= CAL_START - GPS_ACQUIRED_SECONDS:
    #             pressure_kpa[x] = 0.0             

    ####Q is kPa converted to atmospheres
    ####REVISIT REVISIT
    #This pressure term should get pulled from iMet data
    # if len(ambient_pressure_kpa) > 0:
    #     pressure_atm = pressure_kpa/ambient_pressure_kpa
    # else:

    ##I think this is actually just a standard unit conversion from kpa to atm
    pressure_atm = pressure_kpa/101.325;

    #REVISIT REVISIT
    #sound at sea-level
    #Sqrt(gamma*R*T) - Replace with this!
    #T is in Kelvin
    #R is 286 ideal gas constant
    #Gamma is the adiabatic index = 1.4
    if len(temperature_C) == 0:
        temperature_C = 20*np.ones(len(voltage))

    tempK = temperature_C + 273.15
    a_inf = np.sqrt(1.4*286*tempK)

    ##We need to make sure pressure_atm > -1.0
    # for x in range(0,len(pressure_atm)):
    #     if pressure_atm[x] < -1.0:
    #         pressure_atm[x] = -1.0

    # ####This equation here comes from bernoulli
    # 

    #^^^ This is all wrong. Turns out if the pressure is negative it means the velocity is negative
        
    #There is a potential here for
    #k to be less than 0. If that happens, the sqrt goes imaginary
    #Thus we need to add in a fix here
    #So the issue with truncating k at 0 is that when we filter. We
    #loose half of the information. So really what we need to do is
    #filter the bits before we run them through everything
    # for x in range(0,len(k)):
    #     if k[x] < 0.0:
    #         k[x] = 0.0

    #^^^^Same thing this is wrong too

    #This is the rest of the equation from bernoulli. 343.2 is the speed of
    #To fix this we will do a loop
    k = np.copy(pressure_atm)*0
    airspeed_ms = np.copy(pressure_atm)*0
    for x in range(0,len(pressure_atm)):
        #if pressure_atm[x] < -1.0 this never happens. Never mind
        k[x] = 5*((pressure_atm[x]+1.0)**(2.0/7.0)-1.0)
        airspeed_ms[x] = np.sign(k[x])*a_inf[x]*np.sqrt(abs(k[x]))
        #Need to detect nans
        if np.isnan(airspeed_ms[x]):
            airspeed_ms[x] = 0.0
        #print airspeed_ms[x]

    #Ok here's where we need to zero out everything before cal_start
    for x in range(0,len(airspeed_ms)):
        if time_in[x] < cal_end:
            #print "Zeroing..."
            airspeed_ms[x] = 0.0

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

    print('Filtering Signal...')

    ##Run signal through a complimentary filter
    #sigma = 0.03 #Made this an input to the function so we can change it on the fly
    airspeed_ms_filtered = np.zeros(len(airspeed_ms))
    airspeed_ms_filtered[0] = airspeed_ms[0]
    for idx in range(0,len(airspeed_ms)-1):
        airspeed_ms_filtered[idx+1] = (1-sigma)*airspeed_ms_filtered[idx] + sigma*airspeed_ms[idx]
        #print airspeed_ms_filtered[idx+1]
    #airspeed_ms_filtered = deepcopy(airspeed_ms)
    # [airspeed_ms_filtered,filtered_time] = LowPass(airspeed_ms,time_in,wc)
    
    print('Filter Complete')

    #Because conversion from Voltage to speed
    #is still noisy we need to calibrate one more
    #time
    # meanU = 0;
    # numData = 0;
    # for t in tot_time_sec_zero:
    #     if t >= CAL_START and t <= CAL_END:
    #         meanU += airspeed_ms_filtered[numData]
    #         numData += 1
    # if numData == 0:
    #     numData = 1
        
    # airspeed_ms_filtered = airspeed_ms_filtered - meanU/numData
    # print meanU/numData
    #print max(airspeed_ms_filtered)
    #print min(airspeed_ms_filtered)
    #print max(airspeed_ms_filtered)-min(airspeed_ms_filtered)
        
    #RAW SIGNAL
    if debugmode == 1:
        #Raw Bits
        plt.figure()
        plt.plot(time_in,raw_bits,label='Raw')
        #plt.plot(time_in,truncated_bits,label='Truncated')
        plt.plot(time_in,filtered_bits,'r-',label='Filtered')
        #plt.plot(time_in,filtered_truncated_bits,label='Filtered+Truncated')
        plt.xlabel('Time (sec)')
        plt.ylabel('Raw Bits - Sensor = '+PitotName[pitoti])
        plt.legend(loc='best')
        plt.grid()
        pp.savefig()
        
        #Voltage
        plt.figure()
        plt.plot(time_in,voltage)
        plt.xlabel('Time (sec)')
        plt.ylabel('Raw Voltage (V) Sensor = '+str(pitoti))
        plt.grid()
        pp.savefig()
            
        #Scaled Voltage
        plt.figure()
        plt.plot(time_in,voltage-meanV)
        plt.xlabel('Time (sec)')
        plt.ylabel('Scaled Voltage (V)')
        plt.grid()
        pp.savefig()

        #Ambient Pressure
        if len(ambient_pressure_kpa) > 0:
            figure1 = plt.figure()
            plt1 = figure1.add_subplot(1,1,1)
            plt1.plot(time_in,ambient_pressure_kpa-ambient_pressure_kpa[0])
            plt1.get_yaxis().get_major_formatter().set_useOffset(False)
            plt1.set_xlabel('Time (sec)')
            plt1.set_ylabel('Change in Ambient Pressure (kPA)')
            plt1.grid()
            pp.savefig()

        #Pressure in Kpa
        plt.figure()
        plt.plot(time_in,pressure_kpa)
        plt.xlabel('Time (sec)')
        plt.ylabel('Biased Pressure (kPA) - Pitot Probe')
        plt.grid()
        pp.savefig()

        plt.figure()
        plt.plot(time_in,pressure_atm)
        plt.xlabel('Time (sec)')
        plt.ylabel('Biased Pressure (ATM) - Pitot Probe')
        plt.grid()
        pp.savefig()

        plt.figure()
        plt.plot(time_in,k)
        plt.xlabel('Time (sec)')
        plt.ylabel('K')
        plt.grid()
        pp.savefig()

    return [airspeed_ms_filtered,airspeed_ms]

if __name__ == "__main__":

    print('Processing Pitot Probe File')

    #Getting input arguments
    if len(sys.argv) < 5:
        print('Not enough input arguments. Need location of file, number of pitot probes, CAL_START (-99 = default), CAL_END')
        
        #Use default filename
        #inputfilename = 'Data_Files/Mesonet_Data_Files/12_15_2016/GPSLOGFOUR.TXT'
        #numPitots = 4
        #NOGPS = 0
        sys.exit()
    else:
        inputfilename = sys.argv[1]
        numPitots = int(sys.argv[2])
        CAL_TIMES = [int(sys.argv[3]),int(sys.argv[4])]
        if len(sys.argv) > 5:
            NOGPS = int(sys.argv[5])
        else:
            NOGPS = 0

    print('Number of Pitot Probes = ',numPitots)

    #inputfilename = 'Data_Files/HOME_EXPERIMENT.TXT'
    #inputfilename = 'Data_Files/GPSLOG00.TXT'
    #inputfilename = 'Data_Files/6_30_2016_Pitot.TXT'

    #PROCESS GPS DATA - DON'T DO THIS ANYMORE
    #I don't need to do this anymore since the Arduino Parses everything for us.
    #data = gps_data(inputfilename) #this saves the data


    #If you want to plot you need to make a global
    SHOWPLOTS = 0 #1 = show plots, 0 = convert to PDF
    pp = PDF(SHOWPLOTS,plt)

    #PROCESS PITOT AND GPS DATA
    sigma = 0.22
    #sigma = 0.03 #Closer to 0 means more filtering
    #CAL_TIMES = [1700,1800] #Set CAL_TIMES = -99 if you want to default to 0,20
    #CAL_TIMES = [-99,0]
    print(CAL_TIMES)
    data = get_pitot_data(inputfilename,numPitots,sigma,CAL_TIMES,1,pp,NOGPS) #1 = debugmode on, if debug mode is on you need to send pp

    if data == 0:
        sys.exit()
    
    print(data[-1]) #to see directory
    data_gps = data[0]
    data_pitot = data[1]

    #Pitot Data - Remember you can just print data_pitot[-1] to see where everything is
    print(data_pitot[-1])
    # tot_time_sec_zero = data[0]
    # airspeed_ms_filtered_all = data[1]
    # airspeed_ms_all = data[2]

    #Create GPS Plots
    print(data_gps[-1])
    hour = int(np.floor(data_gps[2][0]))
    minute = int(np.floor((data_gps[2][0]-hour)*60))
    print("GPS Start = ",hour,':',minute)
    hour = int(np.floor(data_gps[2][-1]))
    minute = int(np.floor((data_gps[2][-1]-hour)*60))
    print("GPS End = ",hour,':',minute,"\n")
    # gps_data needs to be like this
    # lat_vec_np = data[0]
    # lon_vec_np = data[1]
    # tot_time_gps = data[2]
    # x_vec_np = data[3]
    # y_vec_np = data[4]
    # alt_vec_np = data[5]
    # COmpute del_minute
    del_min = np.ceil((data_gps[2][-1]-data_gps[2][0])*60.0/10.0) #number of minutes
    create_gps_plots(data_gps,del_min,pp,False) #this plots it

    create_pitot_plots(data_pitot,numPitots,pp)

    #Create PTH Plots
    data_PTH = data[2]
    #let's print the PTH directory
    print(data_PTH[-1])
    create_PTH_plots([data_PTH],[data_gps],pp)

    ##Plotting windspeed as a function of altitude
    plt.figure()
    alt_vec_np = data_gps[5]
    airspeed_ms_filtered_all = data_pitot[1]
    for pitoti in range(0,numPitots):
        plt.plot(alt_vec_np,airspeed_ms_filtered_all[pitoti],label=PitotName[pitoti])
    plt.xlabel('Altitude, m')
    plt.ylabel('Windspeed, m/s')
    plt.legend()
    plt.grid()
    pp.savefig()
    
    ##Plotting windspeed as function of GPS time
    time_gps_np = data_gps[2]
    
    time_vec_HHMM,xticks = HHMM_Format(time_gps_np,del_min)

    for pitoti in range(0,numPitots):
        figureP = plt.figure()
        pltP = figureP.add_subplot(1,1,1)
        pltP.plot(time_gps_np,airspeed_ms_filtered_all[pitoti],label=PitotName[pitoti])
        pltP.set_xlabel('Time (HH:MM)')
        pltP.set_ylabel('Windspeed, m/s')
        pltP.set_xticks(xticks) #linspace - start,end,number of points
        pltP.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
        pltP.legend()
        axes = plt.gca()
        axes.set_xlim([time_gps_np[0],time_gps_np[-1]])    
        pltP.grid()
        pp.savefig()


    create_text_file(data,'Pitot_Data.out')
        
    #Close pp
    pp.close()

    # print tot_time_sec_zero
    # print airspeed_ms_filtered
    # print airspeed_ms
    



    
    

