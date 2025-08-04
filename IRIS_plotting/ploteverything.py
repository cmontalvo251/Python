#!/usr/bin/python

# Geophysical_Sampling Plot mesonet, pitot, imet and quad

import sys
import os
import getpass
#Import mesonet module
sys.path.append('Mesonet/')
import mesonet as MES
#Import pitot module
sys.path.append('FASTPitot/')
import pitot as FP
#Import imet module 
sys.path.append('iMet/')
import iMet as MET
#Import Quad module
#sys.path.append('Quad/')
import quad as Q #This has moved to BlackBox
#Import Anemometer module
sys.path.append('Anemometer/')
import anemometer as ANEM
#Import extra stuff
import gps as GPS
import mymath as M
from pdf import PDF

def do_everything(FILES,sigma_pitot,numPitots,CAL_TIMES,sigma_anemometer,SHOWPLOTS):

    ##AVERAGES IN MINUTES - make sure to write 1.0 and not 1 otherwise python will think it's an integer
    AVERAGE_TIME = 60.0/60.0
    PLOTRAW = 1 #Set to zero if you just want the averages

    #quadFile,iMetFile,pitotFile,mesonetFile,anemometerFile
    quadFile = FILES[0]
    iMetFile = FILES[1]
    pitotFile = FILES[2]
    mesonetFile = FILES[3]
    anemometerFile = FILES[4]

    ##############Grab Quad Data#########################
    quad_data_all = []
    baroRead_all = []
    gpsRead_all = []
    QUAD = 0
    #quad_marker = ['x','s']
    if type(quadFile) is not list:
        quadFile = [quadFile]
    for qFile in quadFile:
        quad_data_i = Q.get_quad_data(qFile)
        if quad_data_i:
            quad_data_all.append(quad_data_i)
            print "Quad Data Directory = ",quad_data_i[-1]
            baroRead_i = quad_data_i[0]
            baroRead_all.append(baroRead_i)
            print " " 
            print "Barometer Data = ",dir(baroRead_i)
            #baroRead.altitude
            #baroRead.timeSec
            gpsRead_i = quad_data_i[1]
            gpsRead_all.append(gpsRead_i)
            print "GPS Data = ",dir(gpsRead_i)
            print "Data Taken on " + str(gpsRead_i.month) + "/" + str(gpsRead_i.day)
            QUAD += 1
            quad_color = ['b','k']
        else:
            print "No Quad Data"
            QUAD = 0


    ##############Grab iMet Data########################
    np = MET.np
    try:
        print "iMet Functions = ",dir(MET)
        if len(iMetFile) > 1:
            TWO_IMETS = 1
            iMet1 = iMetFile[0]
            iMet2 = iMetFile[1]
            data_imet_ball = MET.getiMetData(iMet1)
            data_imet_ball2 = MET.getiMetData(iMet2)
            data_imet2 = data_imet_ball2[0]
        else:
            TWO_IMETS = 0
            data_imet_ball = MET.getiMetData(iMetFile) 
        print "iMet Data Directory = ",data_imet_ball[-1]
        data_imet = data_imet_ball[0]
        IMET = 1
    except:
        print "No Imet Data"
        print iMetFile
        IMET = 0 

    ##############Grab Pitot Data#######################
    print "Pitot Functions = ",dir(FP)
    #get_pitot_data takes 3 arguments - filename, numPitot Probes, sigma

    #What's I'd like to add is the ability to plot? Save? multiple files at once
    data_pitot_all = []
    data_pitot_gps = []
    data_pitot_pitot = []
    data_pitot_PTH = []
    PITOT = 0
    pitot_color = ['c','y']
    if type(pitotFile) is not list:
        pitotFile = [pitotFile]
    for pFile in pitotFile:
        if type(CAL_TIMES[0]) is not list: ##This means that the first entry in CAL_TIMES is just a number
            CAL_TIMES_i = CAL_TIMES
        else:
            CAL_TIMES_i = CAL_TIMES[PITOT] #This means that CAL_TIMES is a list of lists
            print CAL_TIMES_i
        data_pitot_i = FP.get_pitot_data(pFile,numPitots,sigma_pitot,CAL_TIMES_i)
        if data_pitot_i:
            data_pitot_all.append(data_pitot_i)
            PITOT += 1
            print "Pitot Directory = ",data_pitot_i[-1]
            data_pitot_gps_i = data_pitot_i[0]
            data_pitot_gps.append(data_pitot_gps_i)
            print "Pitot GPS Directory = ",data_pitot_gps_i[-1]
            data_pitot_pitot_i = data_pitot_i[1]
            data_pitot_pitot.append(data_pitot_pitot_i)
            print "Pitot Data Directroy = ",data_pitot_i[-1]
            data_pitot_PTH_i = data_pitot_i[2]
            data_pitot_PTH.append(data_pitot_i[2])
            print "Pitot Temperature/Pressure/Humidity Data = ",data_pitot_PTH_i[-1]
        else:
            PITOT = 0
            print "No Pitot data"
        
    #################Grab Mesonet Data####################
    print "Mesonet Functions = ",dir(MES)
    mes_color = ['g','#98fb98','g','#98fb98']
    mes_marker = ['s','o','*','^']
    try:
        data_mes = MES.get_mesonet_data(mesonetFile) 
        print "Mesonet Data Directory = ",data_mes[-1]
        MESONET = 1
    except:
        print "No Mesonet Data"
        MESONET = 0

    ##Setup PDF
    plt = MES.plt
    pp = PDF(SHOWPLOTS,plt)

    ################Grab Anemometer Data################
    print "Anemometer Functions = ",dir(ANEM)
    ANEMOMETER = 1
    data_anem = ANEM.get_anemometer_data(anemometerFile,sigma_anemometer)
    if data_anem == 0:
        print "No Anemometer Data"
        ANEMOMETER = 0
    else:
        print "Anemometer Directory = ",data_anem[-1]
        data_anem_gps = data_anem[0]
        data_anem_wind = data_anem[1]
        print "Anemometer GPS Directory = ",data_anem_gps[-1]
        print "Anemometer Wind Directory = ",data_anem_wind[-1]
        anem_color = 'r'

    ##############PLOT ALTITUDE VS TIME#################

    figureALT = plt.figure()
    pltALT = figureALT.add_subplot(1,1,1)

    #Mesonet
    if MESONET == 1:
        time_mesonet = data_mes[0]
        altitude_mesonet = data_mes[3]
        pltALT.plot(time_mesonet,altitude_mesonet,color='g',label='Mesonet Tower')
        time_x = time_mesonet
    else:
        print "Skipping Mesonet - Altitude"

    #Quad
    if QUAD:
        for idx in range(0,QUAD):
            time_quad = gpsRead_all[idx].time_quad
            # FP_GPS_START = time_quad[0]
            # FP_GPS_END = time_quad[-1]
            #altitude_MSL_interp uses the accuracy of the barometer whilst the offset of the GPS
            altitude_quad = gpsRead_all[idx].altitude_MSL_interp
            #altitude uses just the GPS which is usually pretty terrible.
            #altitude_quad = gpsRead_all[idx].altitude
            pltALT.plot(time_quad,altitude_quad,color=quad_color[idx],label='Quad'+str(idx))
    else:
        print "Skipping Quad - Altitude"

    #iMet
    try:
        time_imet = data_imet[:,3]
        #print time_imet
        altitude_imet = data_imet[:,6]
        np.set_printoptions(threshold=np.inf)
        pltALT.plot(time_imet,altitude_imet,color='m',label='iMet')
        time_x = time_imet
        if TWO_IMETS:
            time_imet2 = data_imet2[:,3]
            altitude_imet2 = data_imet2[:,6]
            pltALT.plot(time_imet2,altitude_imet2,color='k',label='iMet2')
    except: 
        print "Skipping imet - Altitude"
    
    #Anemometer
    try:
        time_anemometer = data_anem_gps[2]
        altitude_anemometer = data_anem_gps[5]
        pltALT.plot(time_anemometer,altitude_anemometer,color=anem_color,label='Anemometer')
        time_x = time_anemometer
    except:
        print "Skipping anemometer - Altitude"

    #Pitot
    #try:
    FP_GPS_START = 1e20
    FP_GPS_END = 0
    if PITOT:
        time_pitot_gps = []
        altitude_pitot = []
        pitot_pressure_altitude = []
        for idx in range(0,PITOT):
            data_pitot_gps_i = data_pitot_gps[idx]
            time_pitot_gps_i = data_pitot_gps_i[2]
            time_pitot_gps.append(time_pitot_gps_i)
            if time_pitot_gps_i[0] < FP_GPS_START:
                FP_GPS_START = time_pitot_gps_i[0]
            if time_pitot_gps_i[-1] > FP_GPS_END:
                FP_GPS_END = time_pitot_gps_i[-1]
            altitude_pitot_i = data_pitot_gps_i[5]
            altitude_pitot.append(altitude_pitot_i)

            pltALT.plot(time_pitot_gps_i,altitude_pitot_i,color=pitot_color[idx],label='FASTPitot (MSL) '+str(idx))
            
            time_x = time_pitot_gps_i
            data_pitot_PTH_i = data_pitot_PTH[idx]
            #print data_pitot_PTH_i
            pitot_pressure_altitude_i = data_pitot_PTH_i[4]
            pitot_pressure_altitude.append(pitot_pressure_altitude_i)
            
            #if len(pitot_pressure_altitude_i):
            #    pltALT.plot(time_pitot_gps_i,pitot_pressure_altitude_i,color='#000080',label='FASTPitot (AGL) '+str(idx))
    #except:
    else:
        print "Skipping Pitot Data - Altitude"

    ##HH:MM Format
    if time_x[0] < FP_GPS_START:
        FP_GPS_START = time_x[0]
    if time_x[-1] > FP_GPS_END:
        FP_GPS_END = time_x[-1]
    del_min = np.ceil((FP_GPS_END-FP_GPS_START)*60.0/10.0) #number of minutes
    time_x = np.linspace(FP_GPS_START,FP_GPS_END,len(time_x))
    time_vec_HHMM,xticks = GPS.HHMM_Format(time_x,del_min)

    ###Labeling and Stuff
    pltALT.set_xlabel('Time (HH:MM)')
    pltALT.set_ylabel('Altitude (m)')
    pltALT.legend(loc='best')
    #lgd = pltALT.legend(loc='center left',bbox_to_anchor=(1, 0.5))
    pltALT.grid()
    pltALT.set_xticks(xticks) #linspace - start,end,number of points
    pltALT.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = figureALT.gca()
    axes.set_xlim([FP_GPS_START,FP_GPS_END])

    #Get who plotted it.
    username = getpass.getuser()
    pltALT.set_title(username + ' plotted this data')
        
    #axes.set_ylim([0,200])
    #pp.savefig(lgd)
    pp.savefig()

    ##############PLOT LATITUDE VS TIME#################
    
    figure1 = plt.figure()
    plot1 = figure1.add_subplot(1,1,1)

    #Quad
    if QUAD:
        latitude_quad_all = []
        for idx in range(0,QUAD):
            time_quad = gpsRead_all[idx].time_quad
            latitude_quad_i = gpsRead_all[idx].latitude
            latitude_quad_all.append(latitude_quad_i)
            plot1.plot(time_quad,latitude_quad_i,color=quad_color[idx],label='Quad'+str(idx))
    else:
        print "Skipping Quad - Latitude"

    #iMet
    try:
        latitude_imet = data_imet[:,4]
        plot1.plot(time_imet,latitude_imet,color='m',label='iMet')
        if TWO_IMETS:
            latitude_imet2 = data_imet2[:,4]
            plot1.plot(time_imet2,latitude_imet2,color='k',label='iMet2')
    except:
        print "Skipping iMet - Latitude"

    #Pitot
    if PITOT:
        latitude_pitot = []
        for idx in range(0,PITOT):
            data_pitot_gps_i = data_pitot_gps[idx]
            latitude_pitot_i = data_pitot_gps_i[0]
            # print time_pitot_gps[idx]
            # print latitude_pitot_i
            latitude_pitot.append(latitude_pitot_i)
            plot1.plot(time_pitot_gps[idx],latitude_pitot_i,color=pitot_color[idx],label='FASTPitot'+str(idx))
    else:
        print "Skipping Pitot - Latitude"

    #Mesonet
    if MESONET == 1:
        latitude_mesonet = data_mes[1]
        plot1.plot(time_mesonet,latitude_mesonet,color='g',label='Mesonet Tower')
    else:
        print "Skipping Mesonet - Latitude"

    #Anemometer
    if ANEMOMETER:
        latitude_anemometer = data_anem_gps[0]
        plot1.plot(time_anemometer,latitude_anemometer,color=anem_color,label='Anemometer')
    else:
        print "Skipping Anemometer - Latitude"

    plot1.set_xticks(xticks) #linspace - start,end,number of points
    plot1.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    
    plot1.set_xlabel('Time (HH:MM)')
    plot1.set_ylabel('Latitude (deg)')
    plot1.legend(loc='lower right')
    plot1.grid()
    plot1.get_yaxis().get_major_formatter().set_useOffset(False)
    plt.gcf().subplots_adjust(left=0.15)
    axes = plt.gca()
    #axes.set_ylim([min(latitude_pitot)*.999,max(latitude_pitot)*1.001])
    axes.set_xlim([FP_GPS_START,FP_GPS_END])
    pp.savefig()

    #############PLOT LONGITUDE VS TIME##################
    
    figure2 = plt.figure()
    plot2 = figure2.add_subplot(1,1,1)

    #Quad
    if QUAD:
        longitude_quad_all = []
        for idx in range(0,QUAD):
            time_quad = gpsRead_all[idx].time_quad
            longitude_quad_i = gpsRead_all[idx].longitude
            longitude_quad_all.append(longitude_quad_i)
            plot2.plot(time_quad,longitude_quad_i,color=quad_color[idx],label='Quad'+str(idx))
    else:
        print "Skipping Quad data - Longitude"

    #iMet
    try:
        longitude_imet = data_imet[:,5]
        plot2.plot(time_imet,longitude_imet,color='m',label='iMet')
        if TWO_IMETS:
            longitude_imet2 = data_imet2[:,5]
            plot2.plot(time_imet2,longitude_imet2,color='k',label='iMet2')
    except:
        print "skipping imet data - Longitude"

    #Pitot
    if PITOT:
        longitude_pitot = []
        for idx in range(0,PITOT):
            data_pitot_gps_i = data_pitot_gps[idx]
            longitude_pitot_i = data_pitot_gps_i[1]
            longitude_pitot.append(longitude_pitot_i)
            plot2.plot(time_pitot_gps[idx],longitude_pitot_i,color=pitot_color[idx],label='FASTPitot '+str(idx))
    else:
        print "skipping pitot data - longitude"

    #Mesonet
    if MESONET == 1:
        longitude_mesonet = data_mes[2]
        plot2.plot(time_mesonet,longitude_mesonet,color='g',label='Mesonet Tower')
    else:
        print "Skipping Mesonet - Longitude"

    #Anemometer
    if ANEMOMETER:
        longitude_anemometer = data_anem_gps[1]
        plot2.plot(time_anemometer,longitude_anemometer,color=anem_color,label='Anemometer')
    else:
        print "Skipping anemometer - longitude"

    plot2.set_xticks(xticks) #linspace - start,end,number of points
    plot2.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    plot2.set_xlabel('Time (hrs)')
    plot2.set_ylabel('Longitude (deg)')
    plot2.legend(loc='lower right')
    plot2.grid()
    plot2.get_yaxis().get_major_formatter().set_useOffset(False)
    plt.gcf().subplots_adjust(left=0.15)
    axes = plt.gca()
    #axes.set_ylim([min(longitude_pitot)*.999,max(longitude_pitot)*1.001])
    axes.set_xlim([FP_GPS_START,FP_GPS_END])
    pp.savefig()

    #############PLOT LATITUDE VS LONGITUDE################

    figure3 = plt.figure()
    plot3 = figure3.add_subplot(1,1,1)

    #iMet
    try:
        plot3.plot(latitude_imet,longitude_imet,color='m',label='iMet',marker='o')
        latitude_determination = latitude_imet
        longitude_determination = longitude_imet
        if TWO_IMETS:
            plot3.plot(latitude_imet2,longitude_imet2,color='k',label='iMet2',marker='o')
    except:
        print "Skipping iMet - Lat/Lon"

    #Pitot
    if PITOT:
        for idx in range(0,PITOT):
            plot3.plot(latitude_pitot[idx],longitude_pitot[idx],color=pitot_color[idx],label='FASTPitot '+str(idx),marker='o')
            latitude_determination = latitude_pitot[idx]
            longitude_determination = longitude_pitot[idx]
    else:
        print "Skipping pitot - lat vs. lon"

    #Quad
    if QUAD:
        for idx in range(0,QUAD):
            plot3.plot(latitude_quad_all[idx],longitude_quad_all[idx],color=quad_color[idx],label='Quad'+str(idx),marker='x')
            latitude_determination = latitude_quad_all[idx]
            longitude_determination = longitude_quad_all[idx]
    else:
        print "Skipping quad - lat/lon"

    #Anemometer
    if ANEMOMETER:
        plot3.plot(latitude_anemometer,longitude_anemometer,color=anem_color,label='Anemometer',marker='o')
        latitude_determination = latitude_anemometer
        longitude_determination = longitude_anemometer
    else:
        print "Skipping Anemometer - lat/lon"

    #Figure out where this flight took place
    print 'Computing Location of Flight'
    lat_mean = np.mean(latitude_determination)
    lon_mean = np.mean(longitude_determination)
    location_of_flight = 'Not sure'

    #USA Mesonet Tower
    LOC_FLIGHT = 0
    if lat_mean > 30.69 and lat_mean < 30.70:
        if abs(lon_mean) > 88.19 and abs(lon_mean) < 88.20:
            location_of_flight = 'USA Mesonet Tower'
            LOC_FLIGHT = 1
            #Only plot Mesonet tower if it's at the mesonet tower
            #Mesonet
            if MESONET == 1:
                plot3.plot(latitude_mesonet,longitude_mesonet,color='g',label='Mesonet Tower',marker='s')
            else:
                print "Skipping Mesonet - Lat/Lon"

    # Irvington = 30.491691, -88.211951
    if lat_mean < 30.51 and lat_mean > 30.48:
        if abs(lon_mean) > 88.20 and abs(lon_mean) < 88.22:
            location_of_flight = 'Irvington Airfield'

    # Municipal Park = 30.707685, -88.160286
    if lat_mean > 30.69 and lat_mean < 30.71:
        if abs(lon_mean) > 88.15 and abs(lon_mean) < 88.17:
            location_of_flight = 'Municipal Park'

    #Shelby Hall = 30.691643, -88.174720
    if lat_mean > 30.69 and lat_mean < 30.70:
        if abs(lon_mean) > 88.17 and abs(lon_mean) < 88.18:
            location_of_flight = 'Shelby Hall'

    #Plot Settings
    plot3.set_xlabel('Latitude (deg)')
    plot3.set_ylabel('Longitude (deg)')
    plot3.legend(loc = 'best')
    plot3.grid()
    axes = plt.gca()
    plot3.get_yaxis().get_major_formatter().set_useOffset(False)
    plt.gcf().subplots_adjust(left=0.15)
    plot3.get_xaxis().get_major_formatter().set_useOffset(False)
    #axes.set_xlim([latitude_mesonet[0],latitude_mesonet[0]+0.005])
    #axes.set_ylim([longitude_mesonet[0]+0.014-0.006,longitude_mesonet[0]])

    plot3.set_title('Location of Flight = ' + location_of_flight)
    
    pp.savefig()

    ##############PLOT X vs Y##################################
    
    plt.figure()

    #Mesonet
    if MESONET == 1 and LOC_FLIGHT == 1:
        origin = np.asarray([30.694062,-88.194451])
        mesonet_xy = GPS.convertLATLON([latitude_mesonet,longitude_mesonet],origin)
        plt.plot(mesonet_xy[0],mesonet_xy[1],color='g',label='Mesonet Tower',marker='s')
        print latitude_mesonet[0],longitude_mesonet[0]
    else:
        print "Skipping X vs. Y plots. Using Anemometer as origin"
        try: 
            origin = np.asarray([latitude_anemometer[0],longitude_anemometer[1]])
        except:
            print 'Anemometer Origin not found. Using default mesonet GPS coordinates.'
            origin = np.asarray([30.694062,-88.194451])

    #iMet
    try:
        imet_xy = GPS.convertLATLON([latitude_imet,longitude_imet],origin)
        plt.plot(imet_xy[0],imet_xy[1],label='iMet',color='m',marker='o')
        if TWO_IMETS:
            imet_xy2 = GPS.convertLATLON([latitude_imet2,longitude_imet2],origin)
            plt.plot(imet_xy2[0],imet_xy2[1],label='iMet2',color='k',marker='o')
    except:
        print "skipping iMet - X/Y"

    #Pitot
    if PITOT:
        pitot_xy = []
        for idx in range(0,PITOT):
            pitot_xy_i = GPS.convertLATLON([latitude_pitot[idx],longitude_pitot[idx]],origin)
            pitot_xy.append(pitot_xy)
            plt.plot(pitot_xy_i[0],pitot_xy_i[1],label='FASTPitot '+str(idx),color=pitot_color[idx],marker='o')
    else:
        print "skipping pitot - x vs y"

    #Quad
    if QUAD:
        for idx in range(0,QUAD):
            quad_xy = GPS.convertLATLON([latitude_quad_all[idx],longitude_quad_all[idx]],origin)
            plt.plot(quad_xy[0],quad_xy[1],label='Quad'+str(idx),color=quad_color[idx],marker='x')
    else:
        print "skipping quad - x/y"

    #Anemometer
    try:
        anemometer_xy = GPS.convertLATLON([latitude_anemometer,longitude_anemometer],origin)
        plt.plot(anemometer_xy[0],anemometer_xy[1],color=anem_color,label='Anemometer',marker='o')
    except:
        print "skipping aneometer - x/y"

    plt.xlabel('X (m)')
    plt.ylabel('Y (m)')
    plt.legend(loc='best')
    plt.grid()
    axes = plt.gca()
    #axes.set_xlim([latitude_mesonet[0],latitude_mesonet[0]+0.005])
    #axes.set_ylim([longitude_mesonet[0]+0.014-0.006,longitude_mesonet[0]])
    pp.savefig()

    ############PLOT NORTH WINDSPEED VS TIME####################

    figureN = plt.figure()
    pN = figureN.add_subplot(1,1,1)

    #Pitot
    if PITOT:
        westwindspeed_pitot = []
        eastwindspeed_pitot = []
        northwindspeed_pitot = []
        southwindspeed_pitot = []
        for idx in range(0,PITOT):
            data_pitot_pitot_i = data_pitot_pitot[idx]
            airspeed_ms_filtered_all = data_pitot_pitot_i[1]
            if numPitots == 4:
                ##According to the orientation of the quad and the 4 hole pitot sensor we have the following order
                #Pitot Orientation = West,North,South,East (Qaud Ref)
                westwindspeed_pitot_i = airspeed_ms_filtered_all[0]
                northwindspeed_pitot_i = -airspeed_ms_filtered_all[1] #Note that wind coming out of the North is negative in Earth Science Notation
                southwindspeed_pitot_i = airspeed_ms_filtered_all[2]
                eastwindspeed_pitot_i = -airspeed_ms_filtered_all[3] #Note that wind coming out of the East is negative in Earth Science Notation

                westwindspeed_pitot.append(westwindspeed_pitot_i)
                eastwindspeed_pitot.append(eastwindspeed_pitot_i)
                northwindspeed_pitot.append(northwindspeed_pitot_i)
                southwindspeed_pitot.append(southwindspeed_pitot_i) 

                if PLOTRAW:
                    pN.plot(time_pitot_gps[idx],northwindspeed_pitot_i,label='FASTPitot '+str(idx)+' North')
                    pN.plot(time_pitot_gps[idx],southwindspeed_pitot_i,label='FASTPitot '+str(idx)+' South')
                
                #Pitot with 1 minute average
                avg_data = M.averages(time_pitot_gps[idx],northwindspeed_pitot_i,AVERAGE_TIME)
                time_pitot_avg = avg_data[0]
                northwindspeed_pitot_avg = avg_data[1]
                pN.plot(time_pitot_avg,northwindspeed_pitot_avg,marker=mes_marker[0],color=pitot_color[idx],label='FASTPitot '+str(idx)+' North 1 Min Avg')
                
                avg_data = M.averages(time_pitot_gps[idx],southwindspeed_pitot_i,AVERAGE_TIME)
                time_pitot_avg = avg_data[0]
                southwindspeed_pitot_avg = avg_data[1]
                pN.plot(time_pitot_avg,southwindspeed_pitot_avg,marker=mes_marker[1],color=pitot_color[idx],label='FASTPitot '+str(idx)+' South 1 Min Avg')
            else:
                #When using the single hole pitot probe sensor I had the quad pointing east thus the first column is actually east.
                eastwindspeed_pitot = -airspeed_ms_filtered_all[0]
                print "Assuming single pitot probe sensor"
    else:
        print "Skipping Pitot - no data found for NESW"
            
    #Mesonet
    if MESONET == 1:
        north2_np = data_mes[8]
        north10_np = data_mes[9]
        pN.plot(time_mesonet,north2_np,marker=mes_marker[0],color=mes_color[0],label='Mesonet Tower 2m')
        pN.plot(time_mesonet,north10_np,marker=mes_marker[1],color=mes_color[0],label='Mesonet Tower 10m')
    else:
        print "Skipping Mesonet - North South"
        
    ##Plotting Stuff
    pN.set_xlabel('Time (HH:MM)')
    pN.set_ylabel('North-South Windspeed (m/s)')
    pN.legend(loc='best')
    pN.grid()
    pN.set_xticks(xticks) #linspace - start,end,number of points
    pN.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    axes = plt.gca()
    axes.set_xlim([FP_GPS_START,FP_GPS_END])
    pp.savefig()

    ############PLOT EAST/West WINDSPEED VS TIME#####################
    
    figure3 = plt.figure()
    plot3 = figure3.add_subplot(1,1,1)
    
    #Pitot
    if PITOT:
        #Plot east component
        for idx in range(0,PITOT):
            if PLOTRAW:
                plot3.plot(time_pitot_gps[idx],eastwindspeed_pitot[idx],label='FASTPitot '+str(idx)+' West Raw')
            #Pitot with one minute average
            avg_data = M.averages(time_pitot_gps[idx],eastwindspeed_pitot[idx],AVERAGE_TIME)
            time_pitot_avg = avg_data[0]
            eastwindspeed_pitot_avg = avg_data[1]        
            plot3.plot(time_pitot_avg,eastwindspeed_pitot_avg,marker=mes_marker[0],color=pitot_color[idx],label='FASTPitot '+str(idx)+' East 1 Min Avg')


            #plot west component
            if numPitots == 4:
                if PLOTRAW:
                    plot3.plot(time_pitot_gps[idx],westwindspeed_pitot[idx],label='FASTPitot '+str(idx)+' West Raw')
                #1 minute averages
                avg_data = M.averages(time_pitot_gps[idx],westwindspeed_pitot[idx],AVERAGE_TIME)
                time_pitot_avg = avg_data[0]
                westwindspeed_pitot_avg = avg_data[1]
                plot3.plot(time_pitot_avg,westwindspeed_pitot_avg,marker=mes_marker[1],color=pitot_color[idx],label='FASTPitot '+str(idx)+' West 1 Min Avg')
    else:
        print "Skipping pitot data - east/west"

    #Mesonet
    if MESONET == 1:
        east2_np = data_mes[10]
        east10_np = data_mes[11]
        plot3.plot(time_mesonet,east2_np,marker=mes_marker[0],color=mes_color[0],label='Mesonet Tower 2m')
        plot3.plot(time_mesonet,east10_np,marker=mes_marker[1],color=mes_color[0],label='Mesonet Tower 10m')
    else:
        print "Skipping Mesonet Tower - East/West"
        
    plot3.set_xticks(xticks) #linspace - start,end,number of points
    plot3.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    
    plot3.set_xlabel('Time (HH:MM)')
    plot3.set_ylabel('East-West Wind Speed (m/s)')
    plot3.legend(loc='best')
    plot3.grid()
    axes = plt.gca()
    axes.set_xlim([FP_GPS_START,FP_GPS_END])
    pp.savefig()
    
    ##############PLOT TOTAL WINDSPEED######################
    
    figureALL = plt.figure()
    p = figureALL.add_subplot(1,1,1)

    #Mesonet
    if MESONET == 1:
        wind2 = data_mes[4]
        wind10 = data_mes[5]
        p.plot(time_mesonet,wind2,marker=mes_marker[0],color=mes_color[0],label='Mesonet Tower 2m')
        p.plot(time_mesonet,wind10,marker=mes_marker[1],color=mes_color[0],label='Mesonet Tower 10m')
    else:
        print "Skipping Mesonet - Total Wind"
        
    ##Anemometer
    try:
        wind_anemometer = data_anem_wind[3]
        if PLOTRAW:
            p.plot(time_anemometer,wind_anemometer,label='Anemometer Raw')
        ##Plot 1 minute average for anemometer
        avg_data = M.averages(time_anemometer,wind_anemometer,AVERAGE_TIME)
        p.plot(avg_data[0],avg_data[1],color=anem_color,marker='o',label='Anemometer 1 Min Avg')
    except:
        print "Skipping Anemometer - Wind"

    #Pitot Probe
    if numPitots == 4 and PITOT:
        windspeed_pitot = []
        for idx in range(0,PITOT):
            windspeed_pitot_i = np.sqrt(southwindspeed_pitot[idx]**2 + northwindspeed_pitot[idx]**2 + westwindspeed_pitot[idx]**2 + eastwindspeed_pitot[idx]**2)
            if PLOTRAW:
                p.plot(time_pitot_gps[idx],windspeed_pitot_i,label='FASTPitot '+str(idx)+' Raw')
            avg_data = M.averages(time_pitot_gps[idx],windspeed_pitot_i,AVERAGE_TIME)
            windspeed_pitot.append(windspeed_pitot_i)
            if type(CAL_TIMES[0]) is not list: ##This means that the first entry in CAL_TIMES is just a number
                CAL_TIMES_i = CAL_TIMES
            else:
                CAL_TIMES_i = CAL_TIMES[idx] #This means that CAL_TIMES is a list of lists
            p.plot(avg_data[0],avg_data[1],marker=mes_marker[0],color=pitot_color[idx],label='FASTPitot '+str(idx)+'-1 Min Avg-CAL_TIMES = ' + str(CAL_TIMES_i))

    #Plot stuff
    p.set_xticks(xticks) #linspace - start,end,number of points
    p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
    p.set_xlabel('Time (HH:MM)')
    p.set_ylabel('Scalar Wind Speed (m/s)')
    axes = plt.gca()
    axes.set_xlim([FP_GPS_START,FP_GPS_END])
    # x0 = 14.0 + 6.0/60.0
    # xf = 14.0 + 22.0/60.0
    # axes.set_xlim([x0,xf])
    
    #Put the CAL_TIMES and Sigma into here
    #Also want to figure out orientation of pitot probe
    pFile_full_path = pitotFile[0]
    dirs = pFile_full_path.split('/')
    pFile = dirs[-1]
    if len(pFile) > 3:
        orientation = pFile[3]
    else:
        orientation = '?'
    p.set_title(orientation + ' Pitot = ' + str(sigma_pitot) + ' Anem = ' + str(sigma_anemometer))
    
    p.legend(loc='upper right')
    p.grid()

    pp.savefig()

    #####IF WE HAVE PITOT LETS PLOT WINDSPEED VS ALTITUDE
    if PITOT:
        #eastwindspeed_pitot = -airspeed_ms_filtered_all[0]
        #altitude_pitot
        figureALT_Pitot = plt.figure()
        p = figureALT_Pitot.add_subplot(1,1,1)
        for idx in range(0,PITOT):
            p.plot(windspeed_pitot[idx],np.array(pitot_pressure_altitude[idx])+altitude_pitot[idx][0],color=pitot_color[idx],label='FASTPitot '+str(idx))
        p.set_xlabel('Scalar Wind Speed (m/s)')
        p.set_ylabel('Pressure Altitude (m)')
        p.get_yaxis().get_major_formatter().set_useOffset(False)
        plt.gcf().subplots_adjust(left=0.15)
        axes = plt.gca()
        p.grid()
        p.legend()
        pp.savefig()

            
    ####LETS PLOT PRESSURE. IN THE EVENT WE HAVE QUAD OR IMET DATA WE HAVE PRESSURE#######

    ##Extract pressure data from data_pitot_PTH
    pressure_pitot = []
    PTH_PITOT = 0
    if PITOT:
        for idx in range(0,PITOT):
            data_pitot_PTH_i = data_pitot_PTH[idx]
            pressure_pitot_i = data_pitot_PTH_i[2]/10.0 #Divide by 10 to get it to kPa
            if len(pressure_pitot_i) > 0:
                PTH_PITOT = 1
            pressure_pitot.append(pressure_pitot_i)

    #Turns out we now have PTH FROM THE ANEMOMETER AND MESONET AS WELL
    PTH_MESONET = 0
    if MESONET:
        print data_mes[-1]
        press = data_mes[14]
        hum = data_mes[13]
        temp = data_mes[12]
        temp_height = temp[4]
        hum_height = hum[2]
        print press[-1]
        if len(press[0]) > 0:
            PTH_MESONET = 1

    PTH_ANEMOMETER = 0
    if ANEMOMETER:
        print data_anem[-1]
        PTH_data = data_anem[2]
        print PTH_data[-1]
        pressure_anem = PTH_data[2]/10.0 #divide by 10 to get it to Kpa
        temp_anem = PTH_data[1]
        hum_anem = PTH_data[3]
        if len(pressure_anem) > 0:
            PTH_ANEMOMETER = 1

    if IMET or QUAD or PTH_PITOT or PTH_MESONET or PTH_ANEMOMETER:
        print 'Plotting Pressure'
        figureALL = plt.figure()
        p = figureALL.add_subplot(1,1,1)
        if IMET:
            pressure_imet = data_imet[:,0]
            p.plot(time_imet,pressure_imet,color='m',label='iMet')
            if TWO_IMETS:
                pressure_imet2 = data_imet2[:,0]
                p.plot(time_imet2,pressure_imet2,color='k',label='iMet2')
        if QUAD:
            for idx in range(0,QUAD):
                pressure_quad = baroRead_all[idx].pressurekPA
                time_baro = baroRead_all[idx].timeHr_GPS
                #print pressure_quad
                p.plot(time_baro,pressure_quad,color=quad_color[idx],label='Quad '+str(idx))
        if PTH_PITOT > 0:
            print "plotting PITOT Pressure"
            for idx in range(0,PITOT):
                #print pressure_pitot[idx]
                p.plot(time_pitot_gps[idx],pressure_pitot[idx],color=pitot_color[idx],label='FASTPitot '+str(idx))
        if PTH_ANEMOMETER:
            p.plot(time_anemometer,pressure_anem,color=anem_color,label='Anemometer')
        if PTH_MESONET:
            for i in range(0,2):
                #print press[i]
                plt.plot(time_mesonet,press[i]/10.0,color=mes_color[0],marker=mes_marker[i],label='Mesonet Tower '+str(i))
        p.set_xticks(xticks) #linspace - start,end,number of points
        p.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
        p.set_xlabel('Time (HH:MM)')
        p.set_ylabel('Pressure (kPa)')
        p.get_yaxis().get_major_formatter().set_useOffset(False)
        plt.gcf().subplots_adjust(left=0.15)
        axes = plt.gca()
        axes.set_xlim([FP_GPS_START,FP_GPS_END])
        p.legend(loc='best')
        p.grid()

        pp.savefig()

        #Plot temperature and humidity
        if PTH_PITOT or PTH_ANEMOMETER or PTH_MESONET:
            print 'Plotting Temperature'
            figureTemp = plt.figure()
            pC = figureTemp.add_subplot(1,1,1)
            temperature_pitot = []
            if PTH_PITOT:
                for idx in range(0,PITOT):
                    data_pitot_PTH_i = data_pitot_PTH[idx]
                    temperature_pitot_i = data_pitot_PTH_i[1]
                    temperature_pitot.append(temperature_pitot_i)
                    pC.plot(time_pitot_gps[idx],temperature_pitot_i,color=pitot_color[idx],label='FASTPitot '+str(idx))
            if PTH_ANEMOMETER:
                pC.plot(time_anemometer,temp_anem,color=anem_color,label='Anemometer')
            if PTH_MESONET:
                for i in range(0,4):
                    plt.plot(time_mesonet,temp[i],color=mes_color[0],marker=mes_marker[i],label='Mesonet Tower '+str(temp_height[i])+' m')
            pC.set_xticks(xticks) #linspace - start,end,number of points
            pC.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
            pC.set_xlabel('Time (HH:MM)')
            pC.set_ylabel('Temperature (C)')
            pC.get_yaxis().get_major_formatter().set_useOffset(False)
            plt.gcf().subplots_adjust(left=0.15)
            axes = plt.gca()
            axes.set_xlim([FP_GPS_START,FP_GPS_END])
            pC.legend(loc='best')
            pC.grid()
            pp.savefig()

            print 'Plotting Humidity'
            figureHum = plt.figure()
            pH = figureHum.add_subplot(1,1,1)
            humidity_pitot = []
            if PTH_PITOT:
                for idx in range(0,PITOT):
                    data_pitot_PTH_i = data_pitot_PTH[idx]
                    humidity_pitot_i = data_pitot_PTH_i[3]
                    humidity_pitot.append(humidity_pitot_i)
                    pH.plot(time_pitot_gps[idx],humidity_pitot_i,color=pitot_color[idx],label='FASTPitot '+str(idx))
            if PTH_ANEMOMETER:
                pH.plot(time_anemometer,hum_anem,color=anem_color,label='Anemometer')
            if PTH_MESONET:
                for i in range(0,len(hum_height)):
                    pH.plot(time_mesonet,hum[i],color=mes_color[0],marker=mes_marker[i],label='Mesonet Tower '+str(hum_height[i])+' m')
            pH.set_xticks(xticks) #linspace - start,end,number of points
            pH.set_xticklabels(time_vec_HHMM,rotation=0,ha='right',fontsize=12)
            pH.set_xlabel('Time (HH:MM)')
            pH.set_ylabel('Humidity (%)')
            pH.get_yaxis().get_major_formatter().set_useOffset(False)
            plt.gcf().subplots_adjust(left=0.15)
            axes = plt.gca()
            axes.set_xlim([FP_GPS_START,FP_GPS_END])
            pH.legend()
            pH.grid()
            pp.savefig()

        if PTH_PITOT or QUAD:
            figureALT_Temp = plt.figure()
            pltALT_Temp = figureALT_Temp.add_subplot(1,1,1)
            if PTH_PITOT:
                for idx in range(0,PITOT):
                    pltALT_Temp.plot(temperature_pitot[idx],np.array(pitot_pressure_altitude[idx])+altitude_pitot[idx][0],color=pitot_color[idx],label='FASTPitot '+str(idx))
            ###Labeling and Stuff
            pltALT_Temp.set_xlabel('Temperature (C)')
            pltALT_Temp.set_ylabel('Pressure Altitude (m)')
            pltALT_Temp.legend(loc='best')
            pltALT_Temp.grid()
            pp.savefig()
            print 'Plotting Temp vs Alt'

            figureALT_Press = plt.figure()
            pltALT_Press = figureALT_Press.add_subplot(1,1,1)
            if PTH_PITOT:
                for idx in range(0,PITOT):
                    pltALT_Press.plot(pressure_pitot[idx],altitude_pitot[idx],color=pitot_color[idx],label='FASTPitot '+str(idx))
            #if QUAD:
            #    for idx in range(0,QUAD):
            #        pltALT_Press.plot(baroRead_all[idx].pressurekPA,baroRead_all[idx].altitude_MSL_np,color=quad_color[idx],marker='s',label='Quad '+str(idx))
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
            if PTH_PITOT:
                for idx in range(0,PITOT):
                    pltALT_Hum.plot(humidity_pitot[idx],np.array(pitot_pressure_altitude[idx])+altitude_pitot[idx][0],color=pitot_color[idx],label='FASTPitot '+str(idx))
            ###Labeling and Stuff
            pltALT_Hum.set_xlabel('Relative Humidity (%)')
            pltALT_Hum.set_ylabel('Pressure Altitude (m)')
            pltALT_Hum.legend(loc='best')
            pltALT_Hum.grid()
            pp.savefig()
            print 'Plotting Humidity vs Alt'
            
    ########################################################

    #Create log files for pitot and quad
    if QUAD:
        for idx in range(0,QUAD):
            Q.create_text_file(quad_data_all[idx],'Quad_Data'+str(idx)+'.out')
    if PITOT:
        for i in range(0,PITOT):
            pitot_data = data_pitot_all[i]
            FP.create_text_file(pitot_data,'Pitot_Data'+str(i)+'.out')
    
    pp.close()

if __name__ == "__main__":

    print "Every Module Loaded Successfully"

    ###############Quad FileName################

    quadFile = "Quad/Data_Files/10_25_2016/Flight1.log" #1-4 for October 25 #1-4 corresponds to 53-56 for pitot sensor
    #quadFile = ["Quad/Data_Files/10_25_2016/Flight1.log","Quad/Data_Files/10_25_2016/Flight2.log"] #1-4 for October 25 #1-4 corresponds to 53-56 for pitot sensor
    #quadFile = "Quad/Data_Files/11_29_2016/Flight2.log"
    #quadFile = 'Quad/Data_Files/Quad_Files_3_2_17/ALLFILES.log' #Thurs March Second
    
    ################iMet FileName###############
    #iMetFile = "iMet/Field_Tests/10_25_2016/iMET3-25Oct2016-IrisFront.csv"
    iMetFile = ''

    ################Pitot File Name#############
    #pitotFile = "FASTPitot/Data_Files/Mesonet_Data_Files/10_25_2016/GPSLOG53.TXT" #53-56 for October 25 #53-56 corresponds to flight 1-4 for quad
    pitotFile = ["FASTPitot/Data_Files/Mesonet_Data_Files/10_25_2016/GPSLOG53.TXT","FASTPitot/Data_Files/Mesonet_Data_Files/10_25_2016/GPSLOG54.TXT"]
    #pitotFile = "FASTPitot/Data_Files/Mesonet_Data_Files/11_8_2016/GPSLOG75.TXT"
    #pitotFile = "FASTPitot/Data_Files/Mesonet_Data_Files/11_15_2016/GPSLOG78.TXT"
    #pitotFile = ["FASTPitot/Data_Files/Mesonet_Data_Files/11_29_2016/GPSLOG05.TXT"]
    #pitotFile = ["FASTPitot/Data_Files/PTH_Tests/GPSLOG13.TXT","FASTPitot/Data_Files/PTH_Tests/GPSLOG14.TXT"]
    #pitotFile = "FASTPitot/Data_Files/PTH_Tests/GPSLOG13.TXT" #Thurs March 2 at Mesonet
    #pitotFile = ''
    sigma_pitot = 0.03 #Closer to 0 means more filtering
    CAL_TIMES = [-99,0]
    numPitots = 4

    ##############Mesonet File Name###########
    mesonetFile = "Mesonet/Data_Files/mobileusaw_2016-10-25_2016-10-25.csv"
    #mesonetFile = "Mesonet/Data_Files/mobileusaw_2016-11-08_2016-11-08.csv" #Only 1 file for october 25
    #mesonetFile = "Mesonet/Data_Files/mobileusaw_2016-11-15_2016-11-15.csv"
    #mesonetFile = "Mesonet/Data_Files/mobileusaw_2016-11-22_2016-11-22.csv"
    #mesonetFile = "Mesonet/Data_Files/mobileusaw_2016-11-29_2016-11-29.csv"
    #mesonetFile = 'Mesonet/Data_Files/mobileusaw_2017-03-02_2017-03-02.csv'
    #mesonetFile = 'Mesonet/Data_Files/mobileusaw_2017-03-30_2017-03-30.csv'

    ##############Grab Anemometer Data########
    sigma_anemometer = 0.03 #Closer to 0 means more filtering
    #anemometerFile = 'Anemometer/Data_Files/GPSLOG08.TXT'
    #anemometerFile = 'Anemometer/Data_Files/11_22_2016/GPSLOG09.TXT'
    #anemometerFile = 'Anemometer/Data_Files/Municipal_Park_Tests/3_3_2017/GPSLOG15.TXT'
    #anemometerFile = 'Anemometer/Data_Files/PTH_Tests/With_PTH.TXT'
    anemometerFile = ''

    ###Run the plotting script
    SHOWPLOTS = 0 #1 = show plots, 0 = convert to PDF
    FILES = [quadFile,iMetFile,pitotFile,mesonetFile,anemometerFile]
    do_everything(FILES,sigma_pitot,numPitots,CAL_TIMES,sigma_anemometer,SHOWPLOTS)
