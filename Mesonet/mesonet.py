#!/usr/bin/python
import sys
sys.path.append('c:/users/brandon/git/Geophysical_Sampling')
import numpy as np
import matplotlib.pyplot as plt
from pdf import PDF
from gps import *

def get_mesonet_data(filename):
    try:
        datafile = open(filename)
    except:
        print 'Data File Not Found: ',filename
        return None

    # Here is the link. 
    # http://chiliweb.southalabama.edu/archived_data.php

    # You want to select the following fields
    # Begin and End Date should be the same
    # Station: Mobile (USA Campus West)
    # Format: CSV

    # Files I've Downloaded
    # Timestamp - 0
    # Year - 1
    # Month - 2
    # Day of Month - 3
    # Hour - 4 
    # Minute - 5
    # Latitude - 6
    # Longitude - 7
    # Elevation - 8
    # Scalar Average Wind Speed (m/s) at 2m - 9
    # Direction of resultant windspeed vector (deg) at 2m - 10
    # Scalar Average Wind Speed (m/s) at 10m - 11
    # Direction of resultant windspeed vector (deg) at 10m - 12

    # If you download - Temperature, humidity and pressure the code will interpret the following
    # Files I've Downloaded
    # Timestamp - 0   ... included in data file. no need to select from chili
    # Year - 1
    # Month - 2
    # Day of Month - 3
    # Hour - 4 
    # Minute - 5
    # Latitude - 6
    # Longitude - 7
    # Elevation - 8
    # Air Temp 1.5m - 9
    # Air Temp 2m - 10
    # Air Temp 9.5m - 11
    # Air Temp 10m - 12
    # Rel Hum 2m - 13
    # Rel Hum 10m - 14
    # Air Pressure (1) - 15
    # Air Pressure (2) - 16
    # Scalar Average Wind Speed (m/s) at 2m - 17
    # Direction of resultant windspeed vector (deg) at 2m - 18
    # Scalar Average Wind Speed (m/s) at 10m - 19
    # Direction of resultant windspeed vector (deg) at 10m - 20

    # Sytske's Files - CampusWest-*.csv
    # Timestamp - 0
    # Year - 1 
    # Month - 2
    # Day of Month - 3
    # Hour - 4 
    # Minute - 5
    # Latitude - 6 
    # Longitude - 7
    # Elevation - 8
    # 1.5 m T - 9
    # 2 m T - 10
    # 9.5 m T - 11
    # 10 m T - 12
    # 2 m RH - 13
    # 10 m RH - 14
    # pressure 1 - 15 
    # pressure 2 - 16
    # Total radiation - 17
    # PAR - 18
    # Vertical wind speed - 19
    # Scalar mean wind speed at 2 m (WVc_1) - 20
    # Vector mean wind speed at 2 m (WVc_2) - 21
    # Vector mean wind direction at 2 m (WVc_3) - 22
    # Scalar mean wind speed at 10 m (WVc_1) - 23
    # Vector mean wind speed at 10 m (WVc_2) - 24
    # Vector mean wind direction at 10 m (WVc_3) - 25
    
    counter=0;


    lat= []
    lon= []
    windspeed2= [] #Scalar mean wind speed at 2 m (WVc_1) m/s
    windspeed10= [] #Scalar mean wind speed at 10 m (WVc_1)
    timeMin= []
    timeHour= []
    elevation = []
    winddir2 = []
    winddir10 = []
    temp15 = []
    temp2 = []
    temp95 = []
    temp10 = []
    temp = []
    hum2 = []
    hum10 = []
    hum = []
    press1 = []
    press2 = []
    press = []

    for line in datafile:
        if counter>0:
            row= line.split(',')

            timeHour.append(np.float(row[4].strip('"')))
            timeMin.append(np.float(row[5].strip('"')))

            #lat.append(np.float(row[6].strip('"')))
            #lon.append(np.float(row[7].strip('"')))
            lat.append(30.694062) #I pulled these from Google
            lon.append(-88.194451)
            elevation.append(np.float(row[8].strip('"')))
            
            ##For mobileusaw*.csv
            if len(row) > 13:
                windskip = 8
                temp15.append(np.float(row[9].strip('"')))
                temp2.append(np.float(row[10].strip('"')))
                temp95.append(np.float(row[11].strip('"')))
                temp10.append(np.float(row[12].strip('"')))

                hum2.append(np.float(row[13].strip('"')))
                hum10.append(np.float(row[14].strip('"')))

                press1.append(np.float(row[15].strip('"')))
                press2.append(np.float(row[16].strip('"')))
            else:
                windskip = 0

            windspeed2.append(np.float(row[9+windskip].strip('"')))
            winddir2.append(np.float(row[10+windskip].strip('"')))
            windspeed10.append(np.float(row[11+windskip].strip('"')))
            winddir10.append(np.float(row[12+windskip].rstrip('\n').strip('"')))

            ##For Sytske - CampusWest-*.csv
            # windspeed2.append(np.float(row[20]))
            # windspeed10.append(np.float(row[23]))


        counter+=1

    temp15 = np.array(temp15)
    temp2 = np.array(temp2)
    temp95 = np.array(temp95)
    temp10 = np.array(temp10)
    temp_heights = [1.5,2,9.5,10]
    temp_directory = "Temperature 1.5 (0), 2 (1), 9.5 (2), 10 (3) meters (temp[4] is a vector of heights) \n"
    temp = [temp15,temp2,temp95,temp10,temp_heights,temp_directory]

    hum2 = np.array(hum2)
    hum10 = np.array(hum10)
    hum_heights = [2,10]
    hum_directory = "Humidity 2 and 10 m (hum[2] is the heights in meters) \n"
    hum = [hum2,hum10,hum_heights,hum_directory]
    
    press1 = np.array(press1)
    press2 = np.array(press2)
    press_directory = "Pressure = 1 and 2 \n"
    press = [press1,press2,press_directory]

    winddir2_np = np.array(winddir2)
    winddir10_np = np.array(winddir10)
    lat_np=np.array(lat)
    lon_np=np.array(lon)
    windspeed2_np=np.array(windspeed2)
    windspeed10_np=np.array(windspeed10)
    elevation_np = np.array(elevation)
    timeHour_np=np.array(timeHour)+6 #Add 6 because of Central time to GMT
    timeMin_np=np.array(timeMin)
    timetot_np= timeHour_np+timeMin_np/60.0

    #Compute the North Component of Wind
    north2_np = -windspeed2_np*np.cos(winddir2_np*np.pi/180.0)
    north10_np = -windspeed10_np*np.cos(winddir10_np*np.pi/180.0)
    
    #Compute the East Component of Wind
    east2_np = -windspeed2_np*np.cos(winddir2_np*np.pi/180.0-np.pi/2.0)
    east10_np = -windspeed10_np*np.cos(winddir10_np*np.pi/180.0-np.pi/2.0)
    
    #Make a directory for ease of use
    directory = "Directory for Mesonet Data \n" + "timetot_np - 0 \n" + "lat_np - 1 \n" + "lon_np - 2 \n" + "elevation_np - 3 \n" + "windspeed2_np - 4 \n" + "windspeed10_np - 5 \n" + "winddir2_np - 6 \n" + "winddir10_np - 7 \n" + "north2_np - 8 \n" + "north10_np - 9 \n" + "east2_np - 10 \n" + "east10_np - 11 \n" + "Temperature(C) - 12 \n" + "Humidity(%) - 13 \n" + "Pressure(hPa) 14 \n"

    data_ball = [timetot_np,lat_np,lon_np,elevation_np,windspeed2_np,windspeed10_np,winddir2_np,winddir10_np,north2_np,north10_np,east2_np,east10_np,temp,hum,press,directory]
    
    return data_ball

def plot_mesonet_data(data_ball,pp):
    timetot_np = data_ball[0]
    lat_np = data_ball[1]
    lon_np = data_ball[2]
    elevation_np = data_ball[3]
    windspeed2_np = data_ball[4]
    windspeed10_np = data_ball[5]
    winddir2_np = data_ball[6]
    winddir10_np = data_ball[7]
    north2_np = data_ball[8]
    north10_np = data_ball[9]
    east2_np = data_ball[10]
    east10_np = data_ball[11]
    temp = data_ball[12]
    hum = data_ball[13]
    press = data_ball[14]
    #For kicks let's print the directory
    print data_ball[-1]

    time_vec_HHMM,xticks = HHMM_Format(timetot_np,120)

    fig = plt.figure()
    p = fig.add_subplot(1,1,1)
    plt.plot(timetot_np,elevation_np)
    plt.xlabel('Time (hour)')
    plt.ylabel('Elevation AGL (m)')
    p.set_xticks(xticks) 
    p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([timetot_np[0],timetot_np[-1]])    
    plt.grid()
    pp.savefig()
    
    fig = plt.figure()
    p = fig.add_subplot(1,1,1)
    plt.plot(timetot_np,lat_np)
    plt.xlabel('Time (hour)')
    plt.ylabel('Latitude (deg)')
    p.set_xticks(xticks) 
    p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([timetot_np[0],timetot_np[-1]])    
    plt.grid()
    pp.savefig()

    fig = plt.figure()
    p = fig.add_subplot(1,1,1)
    plt.plot(timetot_np,lon_np)
    plt.xlabel('Time (hour)')
    plt.ylabel('Longitude (deg)')
    p.set_xticks(xticks) 
    p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([timetot_np[0],timetot_np[-1]])    
    plt.grid()
    pp.savefig()

    plt.figure()
    plt.plot(lat_np,lon_np,marker='x')
    plt.xlabel('Latitude (deg)')
    plt.ylabel('Longitude (deg)')
    plt.grid()
    pp.savefig()
    
    fig = plt.figure()
    p = fig.add_subplot(1,1,1)
    plt.plot(timetot_np,windspeed2_np,label='2 M')
    plt.plot(timetot_np,windspeed10_np,label='10 M')
    plt.xlabel('Time (hour)')
    plt.ylabel('Windspeed (m/s)')
    p.set_xticks(xticks) 
    p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([timetot_np[0],timetot_np[-1]])    
    plt.legend()
    plt.grid()
    # axes = plt.gca()
    # axes.set_xlim([8,10])
    # axes.set_ylim([0,2])
    pp.savefig()

    fig = plt.figure()
    p = fig.add_subplot(1,1,1)
    plt.plot(timetot_np,winddir2_np,label='2 M')
    plt.plot(timetot_np,winddir10_np,label='10 M')
    plt.xlabel('Time (hour)')
    plt.ylabel('Wind Direction (deg)')
    p.set_xticks(xticks) 
    p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([timetot_np[0],timetot_np[-1]])    
    plt.legend()
    plt.grid()
    # axes = plt.gca()
    # axes.set_xlim([8,10])
    # axes.set_ylim([0,2])
    pp.savefig()

    fig = plt.figure()
    p = fig.add_subplot(1,1,1)
    plt.plot(timetot_np,north2_np,label='2 M')
    plt.plot(timetot_np,north10_np,label='10 M')
    plt.xlabel('Time (hour)')
    plt.ylabel('North-South Wind Speed (m/s)')
    p.set_xticks(xticks) 
    p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([timetot_np[0],timetot_np[-1]])    
    plt.legend()
    plt.grid()
    pp.savefig()

    fig = plt.figure() 
    p = fig.add_subplot(1,1,1)
    plt.plot(timetot_np,east2_np,label='2 M')
    plt.plot(timetot_np,east10_np,label='10 M')
    plt.xlabel('Time (hour)')
    plt.ylabel('East-West Wind Speed (m/s)')
    p.set_xticks(xticks) 
    p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([timetot_np[0],timetot_np[-1]])    
    plt.legend()
    plt.grid()
    pp.savefig()

    ##Print Temperature Directory
    print temp[-1]
    if len(temp[0]) > 0:
        temp_height = temp[4]
        fig = plt.figure()
        p = fig.add_subplot(1,1,1)
        for i in range(0,4):
            plt.plot(timetot_np,temp[i],label='Temperature '+str(temp_height[i])+' m')
        plt.xlabel('Time (hour)')
        plt.ylabel('Temperature (C)')
        p.set_xticks(xticks) 
        p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
        axes = plt.gca()
        axes.set_xlim([timetot_np[0],timetot_np[-1]])    
        plt.legend(loc='best')
        plt.grid()
        pp.savefig()

    ##Print Humidity
    print hum[-1]
    if len(hum[0]) > 0:
        hum_height = hum[2]
        fig = plt.figure()
        p = fig.add_subplot(1,1,1)
        for i in range(0,len(hum_height)):
            plt.plot(timetot_np,hum[i],label='Humidity '+str(hum_height[i])+' m')
        plt.xlabel('Time (hour)')
        plt.ylabel('Humidity (%)')
        p.set_xticks(xticks) 
        p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
        axes = plt.gca()
        axes.set_xlim([timetot_np[0],timetot_np[-1]])    
        plt.legend(loc='best')
        plt.grid()
        pp.savefig()

    ##Print Pressure
    print press[-1]
    if len(press[0]) > 0:
        fig = plt.figure()
        p = fig.add_subplot(1,1,1)
        for i in range(0,2):
            #print press[i]
            plt.plot(timetot_np,press[i],label='Pressure '+str(i))
        plt.xlabel('Time (hour)')
        plt.ylabel('Pressure (hPa)')
        p.set_xticks(xticks) 
        p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
        axes = plt.gca()
        axes.set_xlim([timetot_np[0],timetot_np[-1]])    
        plt.legend(loc='best')
        p.get_yaxis().get_major_formatter().set_useOffset(False)
        plt.grid()
        pp.savefig()
            

if __name__ == "__main__":

#2 Create a mesonet module
#3 Plot windspeed alongside 1
#4 Lat/lon pitot,imet,quad

    #Get input arguments
    if len(sys.argv) < 2:
        print 'Not enough input arguments. Need location of file'
        #sys.exit()
        print 'Using Default inputfilename'
        inputfilename = 'Data_Files/mobileusaw_2016-12-15_2016-12-15.csv'
        print inputfilename
    else:
        inputfilename = sys.argv[1]

    #Setup pdf viewer
    SHOWPLOTS = 0
    pp = PDF(SHOWPLOTS,plt)
    
    #Get mesonet data ball
    mesonet_ball = get_mesonet_data(inputfilename)
    #Plot everything
    plot_mesonet_data(mesonet_ball,pp)
        
    #Close out pdf file
    pp.close()
