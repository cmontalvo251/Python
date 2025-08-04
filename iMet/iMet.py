#!/usr/bin/python

import numpy as np
import sys
#Import pitot processing
#pitot_filename = '/home/carlos/Documents/GitLab_Repos/Research/Geophysical_Sampling/FASTPitot/'
pitot_filename = '../FASTPitot/'
print 'Appending Pitot Probe File Location = ' + pitot_filename
sys.path.append(pitot_filename)
from pitot import *
#Instead of the old
#sys.path.append('/home/carlos/Dropbox/BlackBox/mypy')
#You can now import individual modules because I added my BlackBox.git directory to the PYTHONPATH
from pdf import PDF #this is from BlackBox.git
from gps import * #This is in BlackBox.git 
from plotting import * #This is in BlackBox.git

def getiMetData(inputfilename):
    iMetfid = open(inputfilename)
    data = []
    UPDATE = 0 #Assume stock firmware
    for line in iMetfid:
        if len(line) > 2:
            row = line.split(',')
            ##Alright so iMet updated their firmware and moved a bunch of columns so we need to do some checks now
            if row[0] != "Time":
                #Assuming this goes through ok it means that we need to choose between the new firmware or not
                if UPDATE:
                    #So in this data set we need to make sure we have enough satellites
                    numsats = np.float(row[45])
                    if numsats != 0:
                        pressure = np.float(row[36])/10 #the new firmware is in millibars and needs to be converted to kPa
                        temp = np.float(row[37]) #temp in celsius
                        humidity = np.float(row[38]) #hum in percent
                        temperature_humidity = np.float(row[39]) #temperature that takes humidity into account? Hmmmm.
                        date = row[40]
                        time_raw = row[41]
                        time = NMEA_TIME(time_raw,'hrs')
                        lat = np.float(row[43])
                        lon = np.float(row[42])
                        altitude = np.float(row[44])
                        ##Then proceed as usual
                        #print pressure
                        data_row = np.array([pressure,temp,humidity,time,lat,lon,altitude,numsats,temperature_humidity])
                        #print data_row
                        data.append(data_row)
                else:
                    #print row[0]
                    #first column is the ID
                    idsensor = row[0]
                    #second column is XQ
                    xq = row[1]
                    #third column is pressure*1000
                    pressure = np.float(row[2])/1000 #kPa
                    #fourth is temperature*100 
                    temp = np.float(row[3])/100 #Celsius
                    #5 is humidity
                    humidity = np.float(row[4]) #units?
                    #6 is date
                    date = row[5]
                    #7 is time
                    time_raw = row[6]
                    time = NMEA_TIME(time_raw,'hrs') #%%Mean Greenwich time +5
                    #8 and 9 are lat lon*10^7
                    lat = np.float(row[7])/pow(10,7) #May have to come back to this by using NMEA_LAT_LON? Actually it looks ok. 5/26/2016 I checked with the Google.
                    lon = np.float(row[8])/pow(10,7)
                    #10 is altitude*1000
                    altitude = np.float(row[9])/1000
                    #11 is number of satellites
                    numsats = np.float(row[10])
                    ##Then proceed as usual
                    data_row = np.array([pressure,temp,humidity,time,lat,lon,altitude,numsats])
                    #print data_row
                    data.append(data_row)
            else:
                print "Skipping First row"
                print "Updated Firmware detected"
                UPDATE = 1
                
    directory = "iMet Sensor Data \n" + "All Data Stored in - data[0] \n" + "Pressure - 0,:,0 \n" + "Temperature - 0,:,1 \n" + "Humidity - 0,:,2 \n" + "Time (hrs) - 0,:,3 \n" + "Latitude - 0,:,4 \n" + "Longitude - 0,:,5 \n" + "Altitude - 0,:,6 \n" + "Number of Satellites - 0,:,7 \n"
    data_np = [np.array(data),directory]

    return data_np

def plotLATLONTEMP(data_ball,pp,*therest):
    data = data_ball[0]
    lat = data[:,4]
    lon = data[:,5]
    temp = data[:,1]
    ##Need to get labels working properly
    figure3 = plt.figure('3-D')
    plt3 = figure3.add_subplot(111,projection='3d')
    plt3.plot_wireframe(lat,lon,temp,color='blue',linestyle='solid')
    plt.title('Temp vs. LAT/LON')
    plt3.set_xlabel('Latitude (deg)')
    plt3.set_ylabel('Longitude (deg)')
    plt3.set_zlabel('Temperature (C)')
    plt3.get_yaxis().get_major_formatter().set_useOffset(False)
    plt3.get_xaxis().get_major_formatter().set_useOffset(False)

    if len(therest) > 0:
        data_ball2 = therest[0]
        data2 = data_ball2[0]
        lat2 = data2[:,4]
        lon2 = data2[:,5]
        temp2 = data2[:,1]
        plt3.plot_wireframe(lat2,lon2,temp2,color='red',linestyle='solid')
    
    #ax = plottool3('Temp vs. LAT/LON',lat,lon,temp,'Latitude (deg)','Longitude (deg)','Temperature (C)')
    pp.savefig()
    # labels = range(-10,11)
    # ax.set_yticklabels(labels)
    # ax.set_xticklabels(labels)
    # ax.set_zticklabels(labels)
    plottool(12,'Latitude (deg)','Longitude (deg)','Latitude vs. Longitude')
    plt.plot(lat,lon)
    if len(therest) > 0:
        plt.plot(lat2,lon2)

    pp.savefig()

    #Convert to Meters
    plottool(12,'X (m)','Y (m)','X vs. Y')
    origin = [lat[0],lon[0]]
    xy = convertLATLON([lat,lon],origin)
    plt.plot(xy[0],xy[1])
    if len(therest) > 0:
        xy2 = convertLATLON([lat2,lon2],origin)
        plt.plot(xy2[0],xy2[1])

    pp.savefig()
    

def plotALTITUDE(data_ball,pp,m,*therest):
    data = data_ball[0]
    time = data[:,3]
    altitude = data[:,6]
    pltA = plottool(12,'Time (HH:MM)','Altitude (m)','Altitude vs. Time')
    if m != -99:
        plt.plot(time[0:m],altitude[0:m],color='blue',marker="o",label='Ascent')
        plt.plot(time[m:-1],altitude[m:-1],color='red',marker="o",label='Descent')
    else:
        plt.plot(time,altitude,color='blue',marker="o",label='IMet1')
    GPS_END = time[-1]
    GPS_START = time[0]
    del_min = np.ceil((GPS_END-GPS_START)*60.0/10.0) #number of minutes
    time_vec_HHMM,xticks = HHMM_Format(time,del_min)
    pltA.set_xticks(xticks) 
    pltA.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([time[0],time[-1]])    

    if len(therest) > 0:
        data_ball2 = therest[0]
        data2 = data_ball2[0]
        time2 = data2[:,3]
        altitude2 = data2[:,6]
        plt.plot(time2,altitude2,color='red',marker="o",label='IMet2')        

    plt.legend()
    pp.savefig()

def plotVSTIME(data_ball,pp,col,yaxislabel,title,*therest):
    data = data_ball[0]
    time = data[:,3]
    yaxis = data[:,col]
    if col == -1:
        yaxis = data[:,0]
        yaxis = -(yaxis - yaxis[0])*(27.0/0.40) #pressure altitude conversion

    plti = plottool(12,'Time (HH:MM)',yaxislabel,title)
    plt.plot(time,yaxis,label='IMet1')
    GPS_END = time[-1]
    GPS_START = time[0]
    del_min = np.ceil((GPS_END-GPS_START)*60.0/10.0) #number of minutes
    time_vec_HHMM,xticks = HHMM_Format(time,del_min)
    plti.set_xticks(xticks) 
    plti.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([time[0],time[-1]])

    if len(therest) > 0:
        data_ball2 = therest[0]
        data2 = data_ball2[0]
        time2 = data2[:,3]
        yaxis2 = data2[:,col]
        if col == -1:
            yaxis = data[:,0]
            yaxis2 = -(yaxis2 - yaxis2[0])*(27.0/0.40) #pressure altitude conversion
        plt.plot(time2,yaxis2,label='IMet2')
        plt.legend()

    pp.savefig()

def plotV2TIME(data_ball,pp,col1,col2,yaxislabel,title,legend1,legend2):
    data = data_ball[0]
    time = data[:,3]
    yaxis = data[:,col1]

    plti = plottool(12,'Time (HH:MM)',yaxislabel,title)
    plt.plot(time,yaxis,label=legend1)
    GPS_END = time[-1]
    GPS_START = time[0]
    del_min = np.ceil((GPS_END-GPS_START)*60.0/10.0) #number of minutes
    time_vec_HHMM,xticks = HHMM_Format(time,del_min)
    plti.set_xticks(xticks) 
    plti.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([time[0],time[-1]])

    yaxis2 = data[:,col2]
    plt.plot(time,yaxis2,label=legend2)
    plt.legend()

    pp.savefig()

def plotALT(data_ball,pp,m,idx,ylabel,*therest):
    data = data_ball[0]
    #Get altitude and y data
    yALL = data[:,idx]
    altitudeALL = data[:,6]

    #Get minimum altitude value - this is done in a different routine now
    #mn = np.min(altitudeALL)
    tol = 3.0
    plottool(12,ylabel,'Altitude (m)','Altitude (m) vs. '+ylabel)
    
    #Get rid of ground both on both left and right streams
    if m != -99:
        altitudeL = altitudeALL[0:m]
        yL = yALL[0:m]
        #valL = [x for x in range(0,len(altitudeL)) if altitudeL[x] > m+2*tol]
        #altitudeLL = altitudeL[valL]
        #yLL = yL[valL]

        altitudeR = altitudeALL[m:-1]
        yR = yALL[m:-1]
        #valR = [x for x in range(0,len(altitudeR)) if altitudeR[x] > m+2*tol]
        #altitudeRR = altitudeR[valR]
        #yRR = yR[valR]
        
        #plot it
        plt.plot(yL,altitudeL,color='blue',marker="o",label='Ascent')
        plt.plot(yR,altitudeR,color='red',marker="o",label='Descent')
        plt.legend()
    else:
        plt.plot(yALL,altitudeALL,label='IMet1')


    if len(therest) > 0:
        data_ball2 = therest[0]
        data2 = data_ball2[0]
        altitudeALL2 = data2[:,6]
        yALL2 = data2[:,idx]
        plt.plot(yALL2,altitudeALL2,label='IMet2')
        plt.legend()

    pp.savefig()

def plotWindspeed(pp,inputfilename,numPitots,sigma_pitot,CAL_TIMES):
    print 'Processing Pitot Probe File'
    #data = get_pitot_data(inputfilename,numPitots,pp,1)
    data = get_pitot_data(inputfilename,numPitots,sigma_pitot,CAL_TIMES)

    data_gps = data[0]
    data_pitot = data[1]

    #Create Pitot Probe GPS plots
    create_gps_plots(data_gps,pp,False) #this plots it

    #Create Pitot Plots
    create_pitot_plots(data_pitot,numPitots,pp)

    return data

def plotALTWIND(winddata,altitude,numPitots,pp):
    #Note this is using altitude from the pitot sensor. 
    #If you decide to stitch two separate data streams you
    #will need to interp using the np.interp command
    #time = data[:,3]
    # altitude = data[:,6]
    # altitude_pitot = np.interp(time_pitot_hrs,time,altitude)
    # plottool(12,'Time (hrs)','Altitude (m)','Time Altitude Pitot');
    # plt.plot(time_pitot_hrs,altitude_pitot)
    # pp.savefig()

    time_pitot = winddata[0]
    #The time stuff has all been solved in the process_pitot_data file
    airspeed_ms_filtered_all = winddata[1]
    time_pitot_hrs = winddata[0]
    #print altitude
    m = np.where(altitude == np.max(altitude))[0]
    if len(m) > 0:
        m = m[0]
    print m
    #print len(airspeed_ms_filtered_all)

    plottool(12,'Wind Speed (m/s)','Altitude (m)','Altitude (m) vs. Speed (m/s)')
    skip = 50
    mycolors = ['blue','purple','green','cyan']
    mycolors2 = ['red','black','yellow','orange']
    for x in range(0,numPitots):
        airspeed_ms_filtered = airspeed_ms_filtered_all[x]
        plt.plot(airspeed_ms_filtered[0:m:skip],altitude[0:m:skip],color=mycolors[x],marker="s",label='Ascent')
        plt.plot(airspeed_ms_filtered[m:-1:skip],altitude[m:-1:skip],color=mycolors2[x],marker="s",label='Descent')
    pp.savefig()
        
if __name__ == "__main__":

    SHOWPLOTS = 0 #1 = show plots, 0 = convert to PDF    
    pp = PDF(SHOWPLOTS,plt)

    #data = getiMetData('Flight_Tests/May_26_2016/20160526-113516-00037232.csv')
    #iMetfilename = 'Flight_Tests/April_20_2016/truncated_file.csv'

    if len(sys.argv) > 1:
        iMetfilename = sys.argv[1]
    else:
        print 'iMetFile not given as input argument'
        sys.exit()

    print 'Processing iMet Sensor'
    data_ball = getiMetData(iMetfilename)

    #Print Dictionary
    print data_ball[-1]

    #Plot Lat Lon and Temperature in a 3D plot
    plotLATLONTEMP(data_ball,pp)

    #Now we want to split all data streams between ascent and descent
    #So this assumes that each data set is a sounding so we need to add a -99 flag
    data = data_ball[0]
    m = np.where(data[:,6] == np.max(data[:,6]))[0]
    if type(m) != type(int()):
        #It means that m is an array
        m = m[0]
    
    #Now we can plot Altitude vs. Time using two streams
    plotALTITUDE(data_ball,pp,m)

    #Plot Scaled Altitude vs Time
    plotVSTIME(data_ball,pp,-1,'Pressure Altitude (m)','Pressure Altitude (m) vs. Time (hrs)')

    #Plot Latitude vs. time
    plotVSTIME(data_ball,pp,4,'Latitude (deg)','Latitude (deg) vs. Time (hrs)')

    #Plot longitude vs. time
    plotVSTIME(data_ball,pp,5,'Longitude (deg)','Longitude (deg) vs. Time (hrs)')

    #Plot temperature vs. time
    plotVSTIME(data_ball,pp,1,'Temperature (C)','Temperature (C) vs. Time (hrs)')

    size = data_ball[0].shape
    if size[1] == 9:
        #This means we can plot temperature calibrated with humidity
        #Plot temperature vs. time
        plotVSTIME(data_ball,pp,8,'Temperature Humidity (C)','Temperature Humidity (C) vs. Time (hrs)')
        #We probably want to plot these on the same graph
        plotV2TIME(data_ball,pp,1,8,'Temperature (C)','Temperature (C) vs. Time (hrs)','Temperature','Temperature Humidity')

    #Pressure vs. time
    plotVSTIME(data_ball,pp,0,'Pressure (kPa)','Pressure (kPa) vs. Time (hrs)')

    #Humidity vs. Time
    plotVSTIME(data_ball,pp,2,'Relative Humidity','Relative Humidity vs. Time (hrs)')

    #Now plot Altitude vs. Temp
    plotALT(data_ball,pp,m,1,'Temperature (C)')

    #Now plot Pressure vs. Altitude
    plotALT(data_ball,pp,m,0,'Pressure (kPa)')

    #Humidit vs. Altitude
    plotALT(data_ball,pp,m,2,'Relative Humidity')


    #Finally get Windspeed from pitot sensor
    #inputfilename = '/home/carlos/Documents/GitLab_Repos/Research/Geophysical_Sampling/FASTPitot/SHELBYHALL.TXT'
    if len(sys.argv) > 3:
        #inputfilename = '/home/carlos/Documents/GitLab_Repos/Research/Geophysical_Sampling/FASTPitot/Data_Files/6_30_2016_Pitot.TXT'
        inputfilename = sys.argv[2]
        #numPitots = 1
        numPitots = int(sys.argv[3])

        sigma_pitot = 0.03
        CAL_TIMES = [-99,0]

        #Process Data file
        #Remember that time_avg in process_pitot strongly affects the data set
        pitot_data = plotWindspeed(pp,inputfilename,numPitots,sigma_pitot,CAL_TIMES) #1 is the number of Pitot probes in the data file

        #Plot Windspeed vs. Altitude (This will need some work since we have two separate data streams
        #Better yet let's just change it to use altitude form the pitot sensor
        gpsdata = pitot_data[0]
        winddata = pitot_data[1]
        alt_vec_np = gpsdata[5]
        plotALTWIND(winddata,alt_vec_np,numPitots,pp)
    else:
        print 'No pitot sensor file given or number of pitot sensors not given'

    #CLOSE FILE
    pp.close()    
    

