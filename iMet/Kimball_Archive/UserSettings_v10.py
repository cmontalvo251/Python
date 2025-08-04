#!/usr/bin/python

import numpy as np
#iMETname     = ["Broken","Broken","Broken","IrisFront","RadiationShield","Tower","RadiationShield","Tower","DLBox","DLBox","DLBox"]
#iMET number      0        1          2                  3         4       5           6         7                   8             9                10                  11                   12               13            14            15                16            17            18                   19               20        21      22
iMETname     = ["Broken","Broken","Broken","CHILIquad-LeftRear","Broken","Anemometer","Broken","FASTquad-LeftSide","Broken","CHILIquad-LeftSide","FASTquad-RightRear","FASTquad-LeftRear","FASTquad-Front","FASTquad-Back","Broken","CHILIquad-Front","CHILIquad-Back","Anemometer","CHILIquad-RightRear","RadiationShield","TowerPost","DLBox","DLBox"]
#iMETname = ["Broken","Broken","Broken","Tower","Broken","Tower","Broken","Tower","Broken","Tower","Tower","Tower","Tower","Tower","Broken","Tower","Tower","Tower","Tower","Tower","Tower","Tower","Tower"]
# iMET plot color
plotcoliMET = [       "",""      ,""      ,"turquoise"         ,""      ,"fuchsia",""    ,"lightgreen"       ,""         ,"MediumVioletRed"   ,"Coral"             ,"Pink"             ,"Maroon"        ,"teal"         ,"     "      ,"SlateGray"      ,"darkmagenta",  "Gold",  "GreenYellow"  ,       "cyan"       ,  "seagreen",  "salmon","indigo"]

RHbias =      [99,99,0.00,2.49,0.04,0.04,-2.83,-2.74, 1.42, 1.36,0.02,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.0,0.0,0.0,0.0,0.0]
pbias  =      [99,99,0.00,0.98,0.00,0.00,-0.05,-0.05,-0.04,-0.04,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.0,0.0,0.0,0.0,0.0]

# Select which iMET should be used to plot pressure - it should be one that was on the drone because we need to see when the drone flew.
ipresFAST=7
ipresCHILI=15
# Set the lowest number of the iMETs that are in deployment rotation 
sensor1=3
#Set the number of iMET sensors that are in deployment rotation
sens=22

ino   = np.ndarray((sens+1),dtype=int)
for i in range(sens+1):
    ino[i]=i
# Set missing iMET sensor numbers to 99
ino[0]=99 #Broken
ino[1]=99 #Broken
ino[2]=99 #Broken
ino[3]=99
ino[4]=99 #Broken
#ino[5]=99
ino[6]=99 #Broken
#ino[7]=99
ino[8]=99 #Broken
ino[9]=99
#ino[10]=99
#ino[11]=99
#ino[12]=99
#ino[13]=99
ino[14]=99 #Broken
ino[15]=99
ino[16]=99
ino[17]=99
ino[18]=99
ino[19]=99
ino[20]=99
ino[21]=99
ino[22]=99



# Initialize all arrays for 'minutes' worth of minute data.
# minutes=90
# Set time (x) axis increment in minutes
delx=1
# Set date and start time in CST; ma==ke sure start time is set to when the first iMET started collecting data.
# You can find this by looking in the iMET Excel files and looking at the first row in the file. Subtract 6 hours from the UTC hour.
# For startmin use the first complete minute in the file. E.g. if the earliest time found in the iMET files is 15:05:50 then starthour=9 and startmin=6
date='29Sep2017'
starthour=12
startmin=17
starttime=float(starthour)+float(startmin)/60.
# Set the latest endtime in CST 
# You can find this by looking in the iMET Excel files and using the last row in the file. Subtract 6 hours from the UTC hour.
# For endmin use the last complete minute in the file. E.g. if the latest time found in the iMET files is 15:05:50 then endhour=9 and endmin=4
endhour=12
endmin=39
endtime=float(endhour)+float(endmin)/60.
# Add 2 because the array starts with zero and we count 1 minute ahead because minute averges are recorded at the start of the next minute.
minutes=int((endtime-starttime)*60)+2
campus=1

# Set number of 2m flights
flights2m=0
start2mflight = np.ndarray(flights2m)
end2mflight   = np.ndarray(flights2m)
# Set start and ending 2m flight times in CST; these are the times the quad is actually in the air and at the required altitude.
start2mflight =['10:42','10:56']
end2mflight   =['10:48','11:08']

# Set number of 10m flights
flights10m=0
start10mflight = np.ndarray(flights10m)
end10mflight   = np.ndarray(flights10m)
# Set start and ending 10m flight times in CST; these are the times the quad is actually in the air and at the required altitude.
start10mflight =['10:55','11:10']
end10mflight   =['11:01','11:23']

# Set number of soundings
soundings=4
startsounding = np.ndarray(soundings)
endsounding   = np.ndarray(soundings)
# Set start and ending 2m flight times in CST; these are the times the quad is actually in the air and at the required altitude.
startsounding =['12:18','12:23','12:28','12:34']
endsounding   =['12:23','12:28','12:34','12:41']

# Set towertest=1 if no flights were conducted and iMETS were installed on a stationary tower, otherwise set it to zero.
towertest=0
starttower='13:32'
endtower='14:48'

# Set temperature axis range and increment for plotting
Tmin=25.0
Tmax=36.0
Tinc=0.2
# Set temperature axis range and increment for plotting
TRHmin=29.0
TRHmax=45.0
TRHinc=0.2
# Set RH axis range and increment for plotting
RHmin=20
RHmax=90
RHinc=1
# Set dew point temperature axis range and increment for plotting
Tdmin=12.0
Tdmax=30.0
Tdinc=0.5
# Set pressure axis range and increment for plotting
presmin=1000.0
presmax=1020.0
presinc=0.5
# Set pressure axis range and increment for plotting
latmin=30.69415
latmax=30.69450
latinc=0.00001

# Set temperature difference limits
Tdiffmin=-2.0
Tdiffmax=2.0
Tdiffinc=0.1
# Set radiation limits and acis increment
radmin=0.0
radmax=1200.0
radinc=50.0
# Set number of observations per minute for iMET data
iobs=60

