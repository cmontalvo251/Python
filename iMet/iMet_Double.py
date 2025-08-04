#!/usr/bin/python

# import numpy as np
# import sys
# #Import pitot processing
# #pitot_filename = '/home/carlos/Documents/GitLab_Repos/Research/Geophysical_Sampling/FASTPitot/'
# pitot_filename = '../FASTPitot/'
# print 'Appending Pitot Probe File Location = ' + pitot_filename
# sys.path.append(pitot_filename)
# from pitot import *
# #Instead of the old
# #sys.path.append('/home/carlos/Dropbox/BlackBox/mypy')
# #You can now import individual modules because I added my BlackBox.git directory to the PYTHONPATH
# from pdf import * #this is from 
# from gps import * #This is in BlackBox.git 
# from plotting import * #This is in BlackBox.git
from iMet import * #This should be in the same folder

if __name__ == "__main__":

    pp = SetupPDF()

    if len(sys.argv) > 2:
        iMetfilename = sys.argv[1]
        iMetfilename2 = sys.argv[2]
    else:
        print 'Need 2 iMet Files. Program Quit'
        sys.exit()

    print 'Processing iMet Sensor'
    data_ball = getiMetData(iMetfilename)
    data_ball2 = getiMetData(iMetfilename2)

    #Plot Lat Lon and Temperature in a 3D plot
    plotLATLONTEMP(data_ball,pp,data_ball2)

    #Set m to -99 so we don't separate by ascent and descent
    m = -99

    #Now we can plot Altitude vs. Time using two streams
    plotALTITUDE(data_ball,pp,m,data_ball2)

    #Plot Scaled Altitude vs Time
    plotVSTIME(data_ball,pp,0,'Pressure Altitude (m)','Pressure Altitude (m) vs. Time (hrs)',data_ball2)

    #Plot Latitude vs. time
    plotVSTIME(data_ball,pp,4,'Latitude (deg)','Latitude (deg) vs. Time (hrs)',data_ball2)

    #Plot longitude vs. time
    plotVSTIME(data_ball,pp,5,'Longitude (deg)','Longitude (deg) vs. Time (hrs)',data_ball2)

    #Plot temperature vs. time
    plotVSTIME(data_ball,pp,1,'Temperature (C)','Temperature (C) vs. Time (hrs)',data_ball2)    

    #Now plot Altitude vs. Temp
    plotALT(data_ball,pp,m,1,'Temperature (C)',data_ball2)

    #Now plot Pressure vs. Altitude
    plotALT(data_ball,pp,m,0,'Pressure (kPa)',data_ball2)

    #CLOSE FILE
    PDFFinish(pp)    
    
