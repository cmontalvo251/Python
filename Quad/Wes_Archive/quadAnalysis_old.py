import os

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
        self.timeMS = []
        self.altitude = []
        self.pressure = []
        self.temperature = []

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Class for GPS readings
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

class gps(object):
    def __init__(self):
        self.timeMS = []
        self.numSats = []
        self.latitude = []
        self.longitude = []
        self.altitude = []
        self.speed = []

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Class for GPS readings
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
                gpsRead.timeMS.append(long(splitLine[2]))
                gpsRead.numSats.append(int(splitLine[4]))
                gpsRead.latitude.append(float(splitLine[6]))
                gpsRead.longitude.append(float(splitLine[7]))
                gpsRead.altitude.append(float(splitLine[9]))
                gpsRead.speed.append(float(splitLine[10]))
    except:
        pass
    
    fileObject.close()

else:
    print "Sorry.  Please run the program again."


