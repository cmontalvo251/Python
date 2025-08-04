import numpy as np
iMETname     = ["Broken","Broken","Broken","Fence","Broken","Fence","Broken","Fence","Fence","Fence","Fence","Fence","Fence","Fence","Fence","Fence","Fence","Fence","Fence","Fence","Fence","Fence","Fence"]
# iMET number  0        1           2                3                      4              5           6                   7                 8            9                10                      11               12               13                  14             15              16            17            18                   19               20        21      22
#iMETname = ["Broken","Broken","CHILIquad-Back","CHILIquad-LeftRear","FASTquad-LeftRear","Tower","FASTquad-RightRear","FASTquad-LeftSide","Broken","CHILIquad-LeftSide","FASTquad-RightRear","FASTquad-Leftrear","FASTquad-Front","FASTquad-Back","CHILIquad-Back","CHILIquad-Front","CHILIquad-Back","Tower","CHILIquad-RightRear","Tower","Tower","Tower","Tower"]
plotcoliMET = [       "",""  ,  "Teal"  ,          "DarkGreen"         ,"DarkRed"      ,"Cyan"     ,  "Magenta"         ,"Crimson"       ," "         ,"LawnGreen"   ,"Magenta"               ,"Orange"     ,     "PeachPuff"    ,"Purple"         , "Teal"      ,"PaleGreen"      ,"Teal",          "Gold",  "Olive"  ,       "SlateGrey"       ,  "LightSkyBlue",  "salmon","indigo"]

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
#    ino[i]=i
    ino[i]=99
# Set missing iMET sensor numbers to 99
#ino[2]=2
ino[3]=3
ino[5]=5
#ino[6]=6
ino[7]=7
#ino[8]=8
ino[9]=9
ino[10]=10
ino[11]=11
ino[12]=12
ino[13]=13
#ino[14]=14
ino[15]=15
ino[16]=16
ino[17]=17
ino[18]=18
#ino[19]=19
ino[20]=20
ino[21]=21
ino[22]=22

# Set iMETformat
# 0 is the oldest format where no RH sensor temperature (senstemp) was given and there are 11 clumns (K is the last one)
# 1 is the next newest format that includes an RH sensor temperature (senstemp).
# 2 is the very nwest format that includes an RH sensor temperature (senstemp) and also a bunch of zeroes.
iMETformat   = np.ndarray((sens+1),dtype=int)
for i in range(sens+1):
    iMETformat[i]=99
iMETformat[2]=2
iMETformat[3]=2
iMETformat[4]=2 
iMETformat[5]=2
iMETformat[6]=2
iMETformat[7]=2
iMETformat[8]=2
iMETformat[9]=2
iMETformat[10]=2
iMETformat[11]=2
iMETformat[12]=2
iMETformat[13]=2
iMETformat[14]=2
iMETformat[15]=2
iMETformat[16]=2
iMETformat[17]=1
iMETformat[18]=1
iMETformat[19]=1
iMETformat[20]=2
iMETformat[21]=2
iMETformat[22]=2

# Initialize all arrays for 'minutes' worth of minute data.
# minutes=90
# Set time (x) axis increment in minutes
delx=1
# Set date and start time in CST; ma==ke sure start time is set to when the first iMET started collecting data.
# You can find this by looking in the iMET Excel files and looking at the first row in the file. Subtract 6 hours from the UTC hour.
# For startmin use the first complete minute in the file. E.g. if the earliest time found in the iMET files is 15:05:50 then starthour=9 and startmin=6
date='24Oct2017'
starthour=13
startmin=8
starttime=float(starthour)+float(startmin)/60.
# Set the latest endtime in CST 
# You can find this by looking in the iMET Excel files and using the last row in the file. Subtract 6 hours from the UTC hour.
# For endmin use the last complete minute in the file. E.g. if the latest time found in the iMET files is 15:05:50 then endhour=9 and endmin=4
endhour=14
endmin=21
endtime=float(endhour)+float(endmin)/60.
# Add 2 because the array starts with zero and we count 1 minute ahead because minute averges are recorded at the start of the next minute.
minutes=int((endtime-starttime)*60)+2
campus=1

# Set number of 2m flights
flights2m=0
start2mflight = np.ndarray(flights2m)
end2mflight   = np.ndarray(flights2m)
# Set start and ending 2m flight times in CST; these are the times the quad is actually in the air and at the required altitude.
start2mflight =['08:06','08:34']
end2mflight   =['08:18','08:44']

# Set number of 10m flights
flights10m=0
start10mflight = np.ndarray(flights10m)
end10mflight   = np.ndarray(flights10m)
# Set start and ending 10m flight times in CST; these are the times the quad is actually in the air and at the required altitude.
start10mflight =['08:21','08:48']
end10mflight   =['08:29','08:58']

# Set number of soundings
soundings=0
startsounding = np.ndarray(soundings)
endsounding   = np.ndarray(soundings)
# Set start and ending 2m flight times in CST; these are the times the quad is actually in the air and at the required altitude.
startsounding =['09:16']
endsounding   =['12:52']

# Set towertest=1 if no flights were conducted and iMETS were installed on a stationary tower, otherwise set it to zero.
towertest=1
starttower='13:8'
endtower='14:21'

# Set RH temperature axis range and increment for plotting
TRHmin=17.0
TRHmax=35.0
TRHinc=0.5

# Set temperature axis range and increment for plotting
Tmin=20.0
Tmax=30.0
Tinc=0.2
# Set RH axis range and increment for plotting
RHmin=0
RHmax=80
RHinc=2
# Set dew point temperature axis range and increment for plotting
Tdmin=-3.0
Tdmax=17.0
Tdinc=0.5
# Set pressure axis range and increment for plotting
presmin=1002.0
presmax=1012.0
presinc=0.2

# Set latitude axis range and increment for plotting
latmin=30.3
latmax=30.8
latinc=0.05
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

