import matplotlib.pyplot as plt
import datetime
from matplotlib.dates import DateFormatter

#********************************************************************************
# Functions for time conversions...
#********************************************************************************
#-----------------------------------------------------
# * Return Modified Julian Day given calendar year,
# * month (1-12), and day (1-31).
# * - Valid for Gregorian dates from 17-Nov-1858.
# * - Adapted from sci.astro FAQ.
#-----------------------------------------------------
def DateToMJD(year, month, day):
    return 367 * year - 7 * (year + (month + 9) / 12) / 4 - \
            3 * ((year + (month - 9) / 7) / 100 + 1) / 4 + \
            275 * month / 9 + day + 1721028L - 2400000L


#-----------------------------------------------------
# * Convert Modified Julian Day to calendar date.
# * - Assumes Gregorian calendar.
# * - Adapted from Fliegel/van Flandern ACM 11/#10 p 657 Oct 1968.
#-----------------------------------------------------
def MJDToDate(MJD):
    J = MJD + 2400001L + 68569L
    C = 4 * J / 146097L
    J = J - (146097L * C + 3) / 4
    Y = 4000 * (J + 1) / 1461001L
    J = J - 1461 * Y / 4 + 31
    M = 80 * J / 2447
    day = J - 2447 * M / 80
    J = M / 11
    month = M + 2 - (12 * J)
    year = 100 * (C - 49) + Y + J
    
    return year, month, day



#********************************************************************************
# Classes to hold each set of data.
#********************************************************************************

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Class for barometer readings
#
# CRt = climb rate
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

class barometer(object):
    def __init__(self):
        self.timeMS      = []
        self.altitude    = []
        self.pressure    = []
        self.temperature = []
        
    def establish_units(self):
        self.pressureMB = []
        for i in self.pressure:
            self.pressureMB.append(i / 100.0)
        self.timeSec = []
        for i in self.timeMS:
            self.timeSec.append(i / 1000.0)

        
    def plot_barometer(self, figObj):
        axis1 = figObj.add_subplot(1, 1, 1)
        axis1.plot(self.timeSec, self.pressureMB, color = "blue")
        axis1.set_ylim([1010.0, 1020.0])
        axis1.set_ylabel("Pressure (mb)")
        axis1.set_xlabel("Time (s)")
        axis1.set_title("November 6 drone flight")
        for t1 in axis1.get_yticklabels():
            t1.set_color("blue")
        
        axis2 = axis1.twinx()
        axis2.plot(self.timeSec, self.altitude, color = "red")
        axis2.set_ylim([-2.0, 30.0])
        axis2.set_ylabel("Altitude [??]")
        
        for t1 in axis2.get_yticklabels():
            t1.set_color("red")
        
        

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Class for GPS readings
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

class gps(object):
    def __init__(self):
        self.timeMS_GPS = []
        self.week_GPS   = []
        self.numSats    = []
        self.latitude   = []
        self.longitude  = []
        self.altitude   = []
        self.speed      = []

    def calibrate_time(self):
        self.timeUTC = []
        for i in range(len(self.timeMS_GPS)):
            MJD_DateSpace = self.week_GPS[i] * 7 + (self.timeMS_GPS[i] / 86400000L)
            MJD_Start = DateToMJD(1980, 1, 6) + MJD_DateSpace
            year, month, day = MJDToDate(MJD_Start)
            
            secondsLeft = (self.timeMS_GPS[i] / 1000) % 86400L
            hours = secondsLeft / 3600
            secondsLeft = secondsLeft - hours * 3600
            minutes = secondsLeft / 60
            seconds = secondsLeft - minutes * 60
            milli = self.timeMS_GPS[i] % 1000
            currentDT = datetime.datetime(year, month, day, hours, minutes, seconds, milli)
            self.timeUTC.append(currentDT)            
    
    def plot_latlon(self, figObj):
        axis1 = figObj.add_subplot(1, 1, 1)
        axis1.plot(self.longitude, self.latitude, color = "green")
        rangeLon = max(self.longitude) - min(self.longitude)
        rangeLat = max(self.latitude) - min(self.latitude)

        plt.ticklabel_format(style = "plain", useOffset = False)
        
        axis1.set_title("Lat/Lon during November 6 flight")
        axis1.set_ylabel("Latitude")
        axis1.set_xlabel("Longitude")
        axis1.set_xlim([min(self.longitude) - 0.25 * rangeLon, max(self.longitude) + 0.25 * rangeLon])
        axis1.set_ylim([min(self.latitude) - 0.25 * rangeLat, max(self.latitude) + 0.25 * rangeLat])
        
        axis2 = plt.axes([0.2, 0.7, 0.15, 0.15])
        axis2.plot(self.timeUTC, self.speed, color = "purple")
        axis2.set_title("Speed during November 6 flight", fontsize = 6)
        axis2.set_xlabel("UTC Time", fontsize = 6)
        axis2.set_ylabel("Speed [??]", fontsize = 6)
        axis2.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        axis2.grid(which = "both", axis = "both", color = "gray", linestyle = "dotted", linewidth = 0.5)
        for t1 in axis2.get_yticklabels():
            t1.set_fontsize(6)
        for t1 in axis2.get_xticklabels():
            t1.set_fontsize(6)
            t1.set_rotation(60)
        
        
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Further Class definitions???
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#
#class gps(object):
#    def __init__(self):
#        self.timeMS = []
#        self.numSats = []
#        self.latitude = []
#        self.longitude = []
#        self.altitude = []
#        self.speed = []


##########################################################################################
##########################################################################################
# Main program
#--------------------------------------------------------------------------------

#------------------------------------------------------------
# Request file name to be read-in
#------------------------------------------------------------

fileName = raw_input("Enter the file name you wish to work with: ")

try:
    with open(fileName) as file:
        fileExists = True
except IOError as e:
    print "Unable to open file" #Does not exist OR no read permissions
    fileExists = False

baroRead = barometer()
gpsRead  = gps()

if (fileExists):
    fileObject = open(fileName, "r")
    try:
        for line in fileObject:
            splitLine = line.split(',')
            if (splitLine[0] == "BARO"):
                baroRead.timeMS.append(long(splitLine[1]))
                baroRead.altitude.append(float(splitLine[2]))
                baroRead.pressure.append(float(splitLine[3]))
                baroRead.temperature.append(float(splitLine[4]))
            elif (splitLine[0] == "GPS"):
                gpsRead.timeMS_GPS.append(long(splitLine[2]))
                gpsRead.week_GPS.append(long(splitLine[3]))
                gpsRead.numSats.append(int(splitLine[4]))
                gpsRead.latitude.append(float(splitLine[6]))
                gpsRead.longitude.append(float(splitLine[7]))
                gpsRead.altitude.append(float(splitLine[9]))
                gpsRead.speed.append(float(splitLine[10]))
    except:
        fileObject.close()
        fileExists = False

else:
    print "Sorry.  Please run the program again."

baroRead.establish_units()
gpsRead.calibrate_time()


figure1 = plt.figure(figsize = (11, 8))
baroRead.plot_barometer(figure1)

figure2 = plt.figure(figsize = (11, 8))
gpsRead.plot_latlon(figure2)

plt.show()

