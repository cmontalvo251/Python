#!/usr/bin/python


####Alright here is the FASTLab version of this code. 

##Import a bunch of stuff
import numpy as np
import csv
import matplotlib.pyplot as plt
import math
#from pylab import * Not sure what this is 
import matplotlib.patches as mpatches
import sys
import os
from pdf import PDF #this is from BlackBox.git but I can send it to you if you need it
#from UserSettings import * No longer need this since it's all one code

#I like pdf plots.
pp = PDF(0,plt)

##I believe in input arguments so from now on you have to tell the code which folder to look in
#Ok actually I'll just default to the ./ directory so I don't ruin anyone's day
if len(sys.argv) < 2:
    directory = ''
else:
    directory = sys.argv[1]
    print 'Using ',directory,' directory'

#iMETname     = ["Broken","Broken","Broken","IrisFront","RadiationShield","Tower","RadiationShield","Tower","DLBox","DLBox","DLBox"]
#iMET number      0        1          2                  3         4       5           6         7                   8             9                10                  11                   12               13            14            15                16            17            18                   19               20        21      22
iMETname     = ["Broken","Broken","Broken","CHILIquad-LeftRear","Broken","Anemometer","Broken","FASTquad-LeftSide","Broken","CHILIquad-LeftSide","FASTquad-RightRear","FASTquad-LeftRear","FASTquad-Front","FASTquad-Back","Broken","CHILIquad-Front","CHILIquad-Back","Anemometer","CHILIquad-RightRear","RadiationShield","TowerPost","DLBox","DLBox"]
#iMETname = ["Broken","Broken","Broken","Tower","Broken","Tower","Broken","Tower","Broken","Tower","Tower","Tower","Tower","Tower","Broken","Tower","Tower","Tower","Tower","Tower","Tower","Tower","Tower"]

# iMET plot color - this would be way better with a dictionary but whatever
plotcoliMET = [       "",""      ,""      ,"turquoise"         ,""      ,"fuchsia",""    ,"lightgreen"       ,""         ,"MediumVioletRed"   ,"Coral"             ,"Pink"             ,"Maroon"        ,"teal"         ,"     "      ,"SlateGray"      ,"darkmagenta",  "Gold",  "GreenYellow"  ,       "cyan"       ,  "seagreen",  "salmon","indigo"]

# Again this would be way better with a dictionary or maybe even an iMet class but whatever.
RHbias =      [99,99,0.00,2.49,0.04,0.04,-2.83,-2.74, 1.42, 1.36,0.02,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.0,0.0,0.0,0.0,0.0]
pbias  =      [99,99,0.00,0.98,0.00,0.00,-0.05,-0.05,-0.04,-0.04,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.0,0.0,0.0,0.0,0.0]

# Select which iMET should be used to plot pressure - it should be one that was on the drone because we need to see when the drone flew.
ipresFAST=7 #I don't this will ever change so it's ok to hard code these
ipresCHILI=15 #same with this one - Although Chili is now RSDG 

# Set the lowest number of the iMETs that are in deployment rotation  - Again I think it's ok to have this hardcoded
sensor1=3
#Set the number of iMET sensors that are in deployment rotation - Same
sens=22

##This array here loops through the vector ino and sets everything to the number in the sequence.
##Originally we would then need to set the missing iMets to 99 but that seems silly.
#Instead we will set the entire vector to 99. Then we will loop through the folder given by sys.argv
#and if we find the sensor we'll update that vector accordingly. so we just need to make a vector with 99's in them
ino = np.ndarray((sens+1),dtype=int)*0+99 #All this does is make a vector of 99's

# The date variable used to be set manually but every file in the directory you're searching for has a date stamp.
for root,dirs,files in os.walk(directory):
    #Then we just need to find an iMET file
    for f in files:
        if len(f) > 6:
            if f[0:4] == 'iMET':
                #once we find the iMet file we need to split based on -
                words = f.split('-')
                #The second word is the date
                date = words[1] #remember that vectors in python start at 0
try:
    print 'Date Found: '+date
except:
    print 'Something went wront with finding the date. Probably cannot find the right file or a file name improperly. If it gets bad call'
    print '2512318353.'
    sys.exit()
    
##For debugging purposes
# 0  1  2  3  4   5  6  7 8  9  10 11 12 13 14 --------------------22]
# Using Caroline's data file
#[99 99 99 99 99  5 99  7 99 99 10 11 12 13 99 99 99 99 99 99 99 99 99]
#So according to the debug case Caroline sent me, only imets 5,7,10,11,12, and 13 are working.
#If you look in Flight_Tests/Sep_29_2017/ you'll see that those files exist. What makes this easier is that
#sytske made the naming convention for all sensors standard using the iMETname variable. So all we have to
#do is attempt to open each one and if we find it we're good. Watch

##This loop here simply looks for every file and sets the ino automatically. Done. You're welcome
#Btdubs this loop is extremely inneficient given the fact that you pretty much open every file and then reopen
#them later on but Sytske should have coded this in a long time ago.
#If I have more time I'll overhaul the code even more another day.
ctr = 0
starthour = 100
startmin = 100
endhour = 0
endmin = 0
for f in iMETname:
    #print f
    fname = "iMET%s-%s-%s.csv" % (ctr,date,f)
    try:
        fid = open(directory + fname) #This just tests whether or not the file is here or not
        #Assuming we can open this file let's grab the first row
        first_row = fid.readline()
        first_row_vec = first_row.split(',') #Assume the delimiter is a comma
        #The 41st column is time
        time = first_row_vec[41]
        #Then we need hour and minute
        hms = time.split(':') #this is split by colons
        #If this imet turned on before all other imets we need to grab it's time
        if int(hms[0]) == starthour:
            if (int(hms[1])) < startmin:
                startmin = int(hms[1]) + 1 #add one since Sytske wants the first full minute
        elif int(hms[0]) < starthour:
            starthour = int(hms[0])
            startmin = int(hms[1]) + 1

        #Ok so now let's get the last line
        fid.seek(-1024, os.SEEK_END)
        last_row = fid.readlines()[-1].decode()
        last_row_vec = last_row.split(',')
        time = last_row_vec[41]
        hms = time.split(':')
        if int(hms[0]) == endhour:
            if (int(hms[1])) > endmin:
                endmin = int(hms[1]) + 1 #add one since Sytske wants the first full minute
        elif int(hms[0]) > endhour:
            endhour = int(hms[0])
            endmin = int(hms[1]) + 1

        fid.close()
        ino[ctr] = ctr #Then we update this ino vector accordingly
        print 'iMet ',ctr,' found'
    except:
        ino[ctr] = 99 #This isn't strictly necessary but it fits nicely in here
        #print 'iMet ',ctr,' is missing'
    ctr+=1

starthour-=6 #May need to change this after daylight savings time
endhour-=6 #May need to change this after daylight savings time
print 'Start Hour and Minute Set to: ',starthour,' ',startmin
print 'End Hour and Minute Set to: ',endhour,' ',endmin
print ino

# Initialize all arrays for 'minutes' worth of minute data.
# minutes=90
# Set time (x) axis increment in minutes - I'm assuming this never changes so I'll leave it hardcoded
delx=1

#Ok start hour and start min is also horse poo. Let's get this to update automatically. Since my loop up above loops through
#all files I will have that get the starthour and startmin
#Then we just compute starttime in decimale equivalent
starttime=float(starthour)+float(startmin)/60.

#Same thing with end minute. Just look at the last row in the imet file and do the same thing as starthour and startmin
endtime=float(endhour)+float(endmin)/60.

# Normally the date variable was set here but that's stupid. Every iMET file in the directory
# Has the date in the filename. So all we need to do is find the second word when we separate by
# dashes

# Add 2 because the array starts with zero and we count 1 minute ahead because minute averges are recorded at the start of the next minute.
minutes=int((endtime-starttime)*60)+2

# Yea so this campus file is also dumb just try the two following lines of code
# if it is successful it means campus is 99 otherwise it's 1
try:
    fname = "CampusWest-%s.csv" % (date)
    finCampus = open(directory + fname)
    finCampus.close()
    fname = "CampusWest-1minave-%s.csv" % (date)
    fin1min = open(directory + fname)
    fin1min.close()
    campus = 1
    print 'Campus Files Found. campus = 1'
except:
    print 'Campus Files not found. campus = 99'
    campus = 99

############################FLIGHT SPECIFIC##################

# making this automatic is pretty tough. If I can get everything to
# be automatic except for this I think I'll have done my part.
# Then all you'll have to do is set this stuff

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
starttower='13:32' #caroline uses the pressure plots for this so look for a high-frequency 
endtower='14:48' #spike in the pressure to get start and end times

#####################################################################

# Set number of observations per minute for iMET data
iobs=60

#==============================================================
# This program reads in iMET and campus weather station data and makes comparison timeseries plots
# Nov 2016, Sytske Kimball
# v10 - Edited by Carlos Montalvo to be more user friendly
#==============================================================
 
#==============================================================
# User Settings... 
#==============================================================
# Assume only 3 hours of data are collected (this is an ok assumption because the iMET battery lasts only 80 minutes).
# Plotcolors
plotcolmeso = ["royalblue","navy"]
legendlabelmeso = ["2m T ","10m T ","2 m RH","10 m RH","2 m wind dir","10 m wind dir","2 m wind speed","10 m wind speed","pressure1","pressure2","latitude","1.5m T","9.5m T"]
months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

legendlabeliMET=[]
for i in range(sens+1):
        legendlabeliMET.append('iMET'+str(i)+' '+iMETname[i])

timelabel=["" for i in range(minutes)]
fin=["" for i in range(sens+1)]
# Weather Station Data
#-----------
temp2m   = np.ndarray((minutes),dtype=float)
temp10m  = np.ndarray((minutes),dtype=float)
temp150  = np.ndarray((minutes),dtype=float)
temp950  = np.ndarray((minutes),dtype=float)
speed2m  = np.ndarray((minutes),dtype=float)
speed10m = np.ndarray((minutes),dtype=float)
dir2m    = np.ndarray((minutes),dtype=float)
dir10m   = np.ndarray((minutes),dtype=float)
rh2m     = np.ndarray((minutes),dtype=float)
rh10m    = np.ndarray((minutes),dtype=float)
tdew2m   = np.ndarray((minutes),dtype=float)
tdew10m  = np.ndarray((minutes),dtype=float)
pressure1 = np.ndarray((minutes),dtype=float)
pressure2 = np.ndarray((minutes),dtype=float)
radiation = np.ndarray((minutes),dtype=float)
lattow   = np.ndarray((minutes),dtype=float)
lontow   = np.ndarray((minutes),dtype=float) 
minerror = np.ndarray((minutes),dtype=float) 
maxerror = np.ndarray((minutes),dtype=float) 
minRHerror = np.ndarray((minutes),dtype=float) 
maxRHerror = np.ndarray((minutes),dtype=float)
minperror = np.ndarray((minutes),dtype=float) 
maxperror = np.ndarray((minutes),dtype=float)
mindewerror = np.ndarray((minutes),dtype=float) 
maxdewerror = np.ndarray((minutes),dtype=float)
zeroline = np.ndarray((minutes),dtype=float) 

# iMET data
tempiMETsec = np.ndarray((sens+1,minutes,iobs),dtype=float)
presiMETsec = np.ndarray((sens+1,minutes,iobs),dtype=float)
RHiMETsec   = np.ndarray((sens+1,minutes,iobs),dtype=float)
RHadjustsec = np.ndarray((sens+1,minutes,iobs),dtype=float)
RHtempsec   = np.ndarray((sens+1,minutes,iobs),dtype=float)
latiMETsec  = np.ndarray((sens+1,minutes,iobs),dtype=float)
loniMETsec  = np.ndarray((sens+1,minutes,iobs),dtype=float)
tdewiMETsec = np.ndarray((sens+1,minutes,iobs),dtype=float)
tempiMET = np.ndarray((sens+1,minutes),dtype=float)
presiMET = np.ndarray((sens+1,minutes),dtype=float)
RHiMET   = np.ndarray((sens+1,minutes),dtype=float)
RHadjust = np.ndarray((sens+1,minutes),dtype=float)
RHtemp   = np.ndarray((sens+1,minutes),dtype=float)
latiMET  = np.ndarray((sens+1,minutes),dtype=float)
loniMET  = np.ndarray((sens+1,minutes),dtype=float)
tdewiMET = np.ndarray((sens+1,minutes),dtype=float)
tempave  = np.ndarray((minutes),dtype=float)
RHave    = np.ndarray((minutes),dtype=float)
presave  = np.ndarray((minutes),dtype=float)
tdewave  = np.ndarray((minutes),dtype=float)


#Initialize the full array with NaN to account for varying start times within the first hour and
#varying end times within the third hour. NaN's will not be plotted.
temp2m   = np.full((minutes),np.nan,dtype=float)
temp10m  = np.full((minutes),np.nan,dtype=float)
temp150  = np.full((minutes),np.nan,dtype=float)
temp950  = np.full((minutes),np.nan,dtype=float)
speed2m  = np.full((minutes),np.nan,dtype=float)
speed10m = np.full((minutes),np.nan,dtype=float)
dir2m    = np.full((minutes),np.nan,dtype=float)
dir10m   = np.full((minutes),np.nan,dtype=float)
rh2m     = np.full((minutes),np.nan,dtype=float)
rh10m    = np.full((minutes),np.nan,dtype=float)
tdew2m   = np.full((minutes),np.nan,dtype=float)
tdew10m  = np.full((minutes),np.nan,dtype=float)
radiation = np.full((minutes),np.nan,dtype=float)
pressure1 = np.full((minutes),np.nan,dtype=float)
pressure2 = np.full((minutes),np.nan,dtype=float)
lattow   = np.full((minutes),np.nan,dtype=float)
lontow   = np.full((minutes),np.nan,dtype=float)

#Error margins
minerror = np.full((minutes),-0.3,dtype=float)
maxerror = np.full((minutes),0.3,dtype=float)
minRHerror = np.full((minutes),-5,dtype=float)
maxRHerror = np.full((minutes),5,dtype=float)
minperror = np.full((minutes),-0.02,dtype=float)
maxperror = np.full((minutes),0.02,dtype=float)
zeroline = np.full((minutes),0.0,dtype=float)

# Calculate Tdew errors from T and RH errors
terror=0.3
rherror=5.0
esat=6.1365*math.exp((17.502*terror)/(240.97+terror))
e=rherror*esat/100.0               
tdewerror=240.97*math.log(e/6.1365)/(17.502-math.log(e/6.1365))
mindewerror = np.full((minutes),-1.0*tdewerror,dtype=float)
maxdewerror = np.full((minutes),tdewerror,dtype=float)

# second data
tempiMETsec = np.full((sens+1,minutes,iobs),np.nan,dtype=float)
RHiMETsec   = np.full((sens+1,minutes,iobs),np.nan,dtype=float)
RHadjustsec = np.full((sens+1,minutes,iobs),np.nan,dtype=float)
RHtempsec   = np.full((sens+1,minutes,iobs),np.nan,dtype=float)
presiMETsec = np.full((sens+1,minutes,iobs),np.nan,dtype=float)
latiMETsec  = np.full((sens+1,minutes,iobs),np.nan,dtype=float)
loniMETsec  = np.full((sens+1,minutes,iobs),np.nan,dtype=float)
tdewiMETsec = np.full((sens+1,minutes,iobs),np.nan,dtype=float)
# 1-min averaged data
tempiMET = np.full((sens+1,minutes),np.nan,dtype=float)
RHiMET   = np.full((sens+1,minutes),np.nan,dtype=float)
RHadjust = np.full((sens+1,minutes),np.nan,dtype=float)
RHtemp   = np.full((sens+1,minutes),np.nan,dtype=float)
presiMET = np.full((sens+1,minutes),np.nan,dtype=float)
latiMET  = np.full((sens+1,minutes),np.nan,dtype=float)
loniMET  = np.full((sens+1,minutes),np.nan,dtype=float)
tdewiMET = np.full((sens+1,minutes),np.nan,dtype=float)

# Data averaged over the number of iMET sensors deployed
tempave = np.full((minutes),np.nan,dtype=float)
RHave   = np.full((minutes),np.nan,dtype=float)
presave = np.full((minutes),np.nan,dtype=float)
tdewave = np.full((minutes),np.nan,dtype=float)

# Open iMET input files
for i in range(sens+1):
    if ino[i]!=99:
        fname = "iMET%s-%s-%s.csv" % (ino[i],date,iMETname[i])
        fin[i]  = open(directory + fname)
# Open Mesonet input file
if campus!=99:
    fname = "CampusWest-%s.csv" % (date)
    finCampus = open(directory + fname)
    fname = "CampusWest-1minave-%s.csv" % (date)
    fin1min = open(directory + fname)

for i in range(sens+1):
# Read in iMET data.
    if (ino[i]!=99):
        count=0
        index=0
# Skip header line, by reading it.
        dummy=fin[i].readline()
        for row in fin[i]:
            if(ino[i]==17 or ino[i]==18 or ino[i]==19):
                stringlist=row.split(",")    
                for k in range(len(stringlist)):
                    if (len(stringlist[k])==0):
                        stringlist[k]=np.nan    
                timestamp=stringlist[7]
                indate=stringlist[6]
                year=indate.split('/')[2]
                month=int(indate.split('/')[0])
                day=int(indate.split('/')[1])
    # Convert UTC to CST
                hour=int(timestamp.split(':')[0])-6
                minute=int(timestamp.split(':')[1])  
                time=float(hour)+float(minute)/60. 
                second=int(timestamp.split(':')[2])  
                tempin=float(stringlist[3])/100.
                presin=float(stringlist[2])/100.
                rhin=float(stringlist[4])/10.
                senstemp=float(stringlist[5])/100.
                latin=float(stringlist[8])/10000000.
                lonin=float(stringlist[9])/10000000.
                elevin=(float(stringlist[10])/1000.) - 50.
                satsin=int(stringlist[11])                        
            else:
                stringlist=row.split(",")    
                for k in range(len(stringlist)):
                    if (len(stringlist[k])==0):
                        stringlist[k]=np.nan   
                timestamp=stringlist[41]
                indate=stringlist[40]
                year=indate.split('/')[2]
                month=int(indate.split('/')[0])
                day=int(indate.split('/')[1])
    # Convert UTC to CST
                hour=int(timestamp.split(':')[0])-6
                minute=int(timestamp.split(':')[1])  
                time=float(hour)+float(minute)/60. 
                second=int(timestamp.split(':')[2])  
                presin=float(stringlist[36])
                tempin=float(stringlist[37])
                rhin=float(stringlist[38])
                senstemp=float(stringlist[39])
                latin=float(stringlist[43])
                lonin=float(stringlist[42])
                elevin=float(stringlist[9])
                satsin=int(stringlist[10])        
            if(count==0):
# Check date
                idate=str(day)+months[month-1]+year
                print "Reading iMET ",ino[i],"Date: ",idate," Start Time: ",timestamp
                if(idate!=date):
                    print "WARNING: wrong date (",idate,") for iMET",ino[i]
                    print "timestamp=",timestamp
            index=(hour-starthour)*60+(minute-startmin)
# Diagnostics
#            if(second==59):
#                print "timestamp,hour,minute,second,time,index=",timestamp,hour,minute,second,time,index
# Fill the arrays and perform rough QC (range check only)
            if(0<= index and index<minutes):
                if(rhin>=0 and rhin <=110):
                    RHiMETsec[i,index,second]=rhin+RHbias[i]
                else:
                    RHiMETsec[i,index,second]=np.nan
                if(presin>=980. and presin <= 1040.):
                    presiMETsec[i,index,second]=presin+pbias[i]
                else:
                    presiMETsec[i,index,second]=np.nan
                latiMETsec[i,index,second]=latin
                loniMETsec[i,index,second]=lonin
                if(tempin>=-15. and tempin <=50.0):
                    tempiMETsec[i,index,second]=tempin
                else:
                    tempiMETsec[i,index,second]=np.nan
                RHtempsec[i,index,second]=senstemp   
# Calculate adjusted RH and Tdew using adjusted RH
                if(np.isnan(RHiMETsec[i,index,second]) or np.isnan(tempiMETsec[i,index,second])):
                    RHadjustsec[i,index,second]=np.nan
                    tdewiMETsec[i,index,second]=np.nan
                else:
                    esatsens=6.1365*math.exp((17.502*senstemp)/(240.97+senstemp))
                    esens=(rhin+RHbias[i])*esatsens/100.0 
# Method 1 (see NOTES 12 Sep 2017)
                    RHadjustsec[i,index,second]=(esens/esat)*100.0
# Method 2 (see NOTES 12 Sep 2017)
#                RHadjustsec[i,index,second]=(e/esatsens)*100.0   
# Calculate Tdew using adjusted RH
                    esat=6.1365*math.exp((17.502*tempin)/(240.97+tempin))
                    e=(RHadjustsec[i,index,second])*esat/100.0               
                    if(e <=0.0):
                        tdewiMETsec[i,index,second]=np.nan
#                    print "iMET, second, minute, hour, day, month, year, T, RH, e=",i,second,minute, hour, day, month, year, tempin, rhin, e                    
                    else:
                        tdewiMETsec[i,index,second]=240.97*math.log(e/6.1365)/(17.502-math.log(e/6.1365))      
            count = count + 1    
#            if(tempiMET[5,89]!=nan and i==5 and count<300):
#                print "i,count,index,timestamp,tempin,tempiMET[5,89]=",i,count,index,timestamp,tempin,tempiMET[5,89]
        fin[i].close()
        print "                                                        End Time: ",timestamp
#        print "i,tempiMET[5]=",i,tempiMET
#        print "iMET, index, count, filename=",i,index,count,fin[i]
#calculate 1-min averages
        RHiMET   = np.nanmean(RHiMETsec,axis=2)   
        RHadjust = np.nanmean(RHadjustsec,axis=2)  
        RHtemp   = np.nanmean(RHtempsec,axis=2) 
        presiMET = np.nanmean(presiMETsec,axis=2)
        latiMET  = np.nanmean(latiMETsec,axis=2)
        loniMET  = np.nanmean(loniMETsec,axis=2)
        tempiMET = np.nanmean(tempiMETsec,axis=2)
        tdewiMET = np.nanmean(tdewiMETsec,axis=2)

print "calculate iMET averages"
tempave = np.nanmean(tempiMET,axis=0) 
RHave   = np.nanmean(RHiMET,axis=0)
presave = np.nanmean(presiMET,axis=0) 
tdewave = np.nanmean(tdewiMET,axis=0) 
    
# Read in the weather station data, except T and RH
# Increment the startminute because in the Mesonet data files
# the timestamp refers to data from the preceeding minute; either an average or the instantaneous value at mm:59
startmin=startmin+1
if (startmin==60):
    starthour=starthour+1
    startmin=0
    
if campus!=99:
# read the header line
    dummy=finCampus.readline()
    countcamp=0
    index=0
    for row in finCampus:
# For comma deliminated input:
        stringlist=row.split(",")    
        for k in range(len(stringlist)):
            if (len(stringlist[k])==0):
                stringlist[k]=np.nan
# Start storing the data when it coincides with the iMET observing period.   
        hour=int(stringlist[4])
        minute=int(stringlist[5])
        if(countcamp==0):
# Check date
            timestamp=stringlist[0]
            indate=timestamp.split(' ')[0]
            month=int(indate.split('/')[0])
            day=int(indate.split('/')[1])
            year=indate.split('/')[2]
            idate=str(day)+months[month-1]+year
            if(idate!=date):
                print "WARNING line 259: wrong date (",idate,") for Campus Station"
                print "timestamp=",timestamp
        index=(hour-starthour)*60+(minute-startmin)
        if((hour>starthour or (hour==starthour and minute >= startmin)) and index < minutes):            
#            print "hour,min,index=",hour,minute,index
            pres1in=float(stringlist[15])
            pres2in=float(stringlist[16])
            radin=float(stringlist[17])
            speed2in=float(stringlist[20])
            speed10in=float(stringlist[23])
            dir2in=float(stringlist[22])
            dir10in=float(stringlist[25])
            latin=float(stringlist[6])
            lonin=float(stringlist[7])  
# Fill the arrays
            if(minute<10):
                timelabel[index]=str(hour)+':'+'0'+str(minute)
            else:
                timelabel[index]=str(hour)+':'+str(minute)     
            speed2m[index]=speed2in
            speed10m[index]=speed10in
            dir2m[index]=dir2in
            dir10m[index]=dir10in
            if(pres1in>=980. and pres1in<=1040.):
                pressure1[index]=pres1in
            else:
                pressure1[index]=np.nan
            if(pres2in>=980. and pres2in<=1040.):
                pressure2[index]=pres2in
            else:
                pressure2[index]=np.nan
            radiation[index]=radin
            lattow[index]=latin
            lontow[index]=lonin
        countcamp = countcamp + 1      
    finCampus.close()

# Read in 1-min ave temperature and RH weather station data.
# read the header lines
if campus!=99:
    dummy=fin1min.readline()
    countcamp=0
    index=0
    for row in fin1min:
# For comma deliminated input:
        stringlist=row.split(",")    
        for k in range(len(stringlist)):
            if (len(stringlist[k])==0):
                stringlist[k]=np.nan
# Start storing the data when it coincides with the iMET observing period.   
        hour=int(stringlist[7])
        minute=int(stringlist[8])
        if(countcamp==0):
# Check date
            timestamp=stringlist[0]
            indate=timestamp.split(' ')[0]
            month=int(indate.split('/')[0])
            day=int(indate.split('/')[1])
            year=indate.split('/')[2]
            idate=str(day)+months[month-1]+year
            if(idate!=date):
                print "WARNING: wrong date (",idate,") for 1-min Campus Station"
                print "timestamp=",timestamp
        index=(hour-starthour)*60+(minute-startmin)
        if((hour>starthour or (hour==starthour and minute >= startmin)) and index < minutes):
#            print "hour,min,index=",hour,minute,index
            temp150in=float(stringlist[12])
            temp2in=float(stringlist[13])
            temp950in=float(stringlist[14])
            temp10in=float(stringlist[15])
            rh2in=float(stringlist[16])
            rh10in=float(stringlist[17])
            if(temp150in>=-15.0 and temp150in<=50.0):
                temp150[index]=temp150in
            else:
                temp150[index]=np.nan                
            if(temp950in>=-15.0 and temp950in<=50.0):
                temp950[index]=temp950in
            else:
                temp950[index]=np.nan                
            if(temp2in>=-15.0 and temp2in<=50.0):
                temp2m[index]=temp2in
            else:
                temp2m[index]=np.nan
            if(temp10in>=-15.0 and temp10in<=50.0):
                temp10m[index]=temp10in
            else:
                temp10m[index]=np.nan    
            if(rh2in>=0.5 and rh2in<=110.0):
                rh2m[index]=rh2in
            else:
                rh2m[index]=np.nan                
            if(rh10in>=0.5 and rh10in<=110.0):
                rh10m[index]=rh10in
            else:
                rh10m[index]=np.nan
# Calculate Tdew
            if(np.isnan(temp2m[index])or np.isnan(rh2m[index])):
                tdew2m[index]=np.nan
            else:
                esat=6.1365*math.exp((17.502*temp2in)/(240.97+temp2in))
                e=rh2in*esat/100.0
                if(e <=0.0):
                    tdew2m[index]=np.nan
#                print "iMET, second, minute, hour, day, month, year, T, RH, e=",i,second,minute, hour, day, month, year, tempin, rhin, e                    
                else:
                    tdew2m[index]=240.97*math.log(e/6.1365)/(17.502-math.log(e/6.1365))  
            if(np.isnan(temp10m[index]) or np.isnan(rh10m[index])):
                tdew10m[index]=np.nan
            else:
                esat=6.1365*math.exp((17.502*temp10in)/(240.97+temp10in))
                e=rh10in*esat/100.0
                if(e <=0.0):
                    tdew10m[index]=np.nan
#                print "iMET, second, minute, hour, day, month, year, T, RH, e=",i,second,minute, hour, day, month, year, tempin, rhin, e                    
                else:
                    tdew10m[index]=240.97*math.log(e/6.1365)/(17.502-math.log(e/6.1365))  
        countcamp = countcamp + 1      
    fin1min.close()

# Mesonet averaged data over the entire deployment time
avetemp2m    = np.nanmean(temp2m,axis=0) 
avetemp10m   = np.nanmean(temp10m,axis=0) 
averh2m      = np.nanmean(rh2m,axis=0) 
averh10m     = np.nanmean(rh10m,axis=0)
avespeed2m   = np.nanmean(speed2m,axis=0) 
avespeed10m  = np.nanmean(speed10m,axis=0) 
avepressure  = np.nanmean(pressure1,axis=0) 
averadiation = np.nanmean(radiation,axis=0) 

# If plotting long timeseries, only write every other label, accomplish this by making the label for even minutes blank
#if (minutes>90):
#    for j in range(minutes):
#        if(j % 2 == 0):
#            timelabel[j]=' '

print 'Getting min and max stuff'
#Ok to get min and max we just loop through all the imets
Tmin = 10000
Tmax = -99999
TRHmin = 10000
TRHmax = -99999
RHmin = 10000
RHmax = -9999
Tdmin = 100000
Tdmax = -999999
presmin = 10000000000
presmax = -10000000000
latmin = 90
latmax = 0
for i in range(sens+1):
    if ino[i] != 99:
        #print tempiMET[ino[i]]
        m = np.nanmin(tempiMET[ino[i]])

        if m < Tmin:
            Tmin = m
        m = np.nanmax(tempiMET[ino[i]])
        if m > Tmax:
            Tmax = m
        m = np.nanmin(RHtemp[ino[i]])

        if m < TRHmin:
            TRHmin = m
        m = np.nanmax(RHtemp[ino[i]])
        if m > TRHmax:
            TRHmax = m

        m = np.nanmin(RHiMET[ino[i]])
        if m < RHmin:
            RHmin = m
        m = np.nanmax(RHiMET[ino[i]])
        if m > RHmax:
            RHmax = m

        m = np.nanmin(RHadjust[ino[i]])
        if m < RHmin:
            RHmin = m
        m = np.nanmax(RHadjust[ino[i]])
        if m > RHmax:
            RHmax = m

        m = np.nanmin(tdewiMET[ino[i]])
        if m < Tdmin:
            Tdmin = m
        m = np.nanmax(tdewiMET[ino[i]])
        if m > Tdmax:
            Tdmax = m

        m = np.nanmin(presiMET[ino[i]])
        if m < presmin:
            presmin = m
        m = np.nanmax(presiMET[ino[i]])
        #print m
        if m > presmax:
            presmax = m

        m = np.nanmin(latiMET[ino[i]])
        if m < latmin:
            latmin = m
        m = np.nanmax(latiMET[ino[i]])
        if m > latmax:
            latmax = m

Tmin-=0.1
Tmax+=0.1
Tmin=np.floor(Tmin)
Tmax=np.ceil(Tmax)


TRHmin-=0.1
TRHmax+=0.1
TRHmin=np.floor(TRHmin)
TRHmax=np.ceil(TRHmax)

RHmin-=0.1
RHmax+=0.1
RHmin=np.floor(RHmin)
RHmax=np.ceil(RHmax)

Tdmin-=0.1
Tdmax+=0.1
Tdmin=np.floor(Tdmin)
Tdmax=np.ceil(Tdmax)

presmin-=0.1
presmax+=0.1
presmin=np.floor(presmin)
presmax=np.ceil(presmax)

# These have been switched to automatic functions. 
# Here we go.
Tinc=np.round(0.2*(Tmax-Tmin)/7,1)
# Set temperature axis range and increment for plotting
TRHinc=np.round(0.2*(TRHmax-TRHmin)/7,1)
# Set RH increment for plotting
RHinc=np.round(0.2*(RHmax-RHmin)/7,1)
# Set dew point temperature axis range and increment for plotting
Tdinc=np.round(0.2*(Tdmax-Tdmin)/7,1)
# Set pressure axis range and increment for plotting
presinc=0.5
# Set pressure axis range and increment for plotting
latinc=0.0001

# Set radiation limits and axis increment
radmin=0.0
radmax=1200.0
radinc=50.0


print 'Temperature Min and Max = ',Tmin,Tmax
print 'TRH Min and Max = ',TRHmin,TRHmax
print 'RH Min and Max = ',RHmin,RHmax
print 'Dew Min and Max = ',Tdmin,Tdmax
print 'Press Min and Max = ',presmin,presmax
print 'Latitude Min and Max = ',latmin,latmax
print "Plot Stuff"
          
##Plot temperature data
#######################    
figure1 = plt.figure(figsize = (25, 15))
plot1 = figure1.add_subplot(1,1,1)
# Plot temperature
for i in range(sens+1):
    if ino[i]!=99:
        plot1.plot(range(minutes), tempiMET[ino[i]], linewidth=1.2, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
if campus!=99:
    num=11
    plot1.plot(range(minutes), temp150, linewidth=1.2, linestyle='--', color=plotcolmeso[0], label=legendlabelmeso[num])
    num=0
    plot1.plot(range(minutes), temp2m, linewidth=1.2, color=plotcolmeso[0], label=legendlabelmeso[num])   
    num=12
    plot1.plot(range(minutes), temp950, linewidth=1.2, linestyle='--', color=plotcolmeso[1], label=legendlabelmeso[num])
    num=1
    plot1.plot(range(minutes), temp10m, linewidth=1.2, color=plotcolmeso[1], label=legendlabelmeso[num])    

# strlabels are the minutes used as x axis labels (see set_xticklabels)
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
plot1.set_ylim([Tmin,Tmax])
plot1.set_yticks(np.arange(Tmin,Tmax+0.1,Tinc))
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
plot1.set_ylabel(r"Temperature ($^{o}$C)",fontsize = 18)
plot1.text(1,Tmax+Tinc,"Temperature Comparison %s " % (date),fontsize=22,fontweight='bold')
plot1.grid(which='both',axis='both',color='LightGrey',linestyle='dotted')
plot1.legend(loc=2)

# Write average values:
if (minutes < 30):
    offset=10
else:
    offset=25

inc = (Tmax-Tmin)*0.09214/4.3
plot1.text(minutes-offset,Tmax+4.3*inc,"Average Values:",horizontalalignment='left',fontsize=18,fontweight='bold')
plot1.text(minutes-offset,Tmax+3.3*inc,"2m T = %5.2f $^{o}$C" % (avetemp2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,Tmax+2.3*inc,"10m T = %5.2f $^{o}$C" % (avetemp10m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,Tmax+1.3*inc,"2m RH = %5.2f " % (averh2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,Tmax+0.3*inc,"10m RH = %5.2f " % (averh10m),horizontalalignment='left',fontsize=18,fontweight='normal')

plot1.text(minutes-5,Tmax+3.3*inc,"2m wind = %5.2f m s$^{-1}$" % (avespeed2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,Tmax+2.3*inc,"10m wind = %5.2f m s$^{-1}$" % (avespeed10m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,Tmax+1.3*inc,"pressure = %7.2f mb" % (avepressure),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,Tmax+0.3*inc,"radiation = %5.2f W m$^{-2}$" % (averadiation),horizontalalignment='left',fontsize=18,fontweight='normal')

# Add a right side y axis for Total Radiation.
if campus!=99:
    plot2 = plot1.twinx()
    plot2.plot(range(minutes), radiation, linewidth=1.0, linestyle='--', color='tomato', label="Total Radiation")
    plot2.set_ylim(radmin,radmax)
# Plot iMET pressure (it is always on the quad)
    a=1280/(presmax-presmin)
    b=1300-a*presmax
    plot2.plot(range(minutes), (presiMET[ipresFAST]*a + b), linewidth=1.0, linestyle='-', color='black', label="scaled iMET pressure")
    plot2.plot(range(minutes), (presiMET[ipresCHILI]*a + b), linewidth=1.0, linestyle='-', color='black')
    yticks=[]
    yticks=np.arange(radmin,radmax+0.1,radinc)
    plot2.get_yaxis().get_major_formatter().set_useOffset(False)
# To trim the margins
#tight_layout()
    plot2.set_yticks(yticks)
    for label in plot2.get_yticklabels():
        label.set_color('tomato')
        label.set_size(18)
    plot2.set_ylabel(r"Total Radiation (W m$^{-2}$)",fontsize = 18, color='tomato')
# put legend in upper right corner
    plot2.legend(loc=1)
# Write the plot to a file 
figure1.savefig(directory + "iMET-Tower-TempComparison-%s-1minave.png" % (date))
pp.savefig()
plt.close(figure1)
print 'One figure down'

##Plot RH sensor temperature data
#################################    
figure1 = plt.figure(figsize = (25, 15))
plot1 = figure1.add_subplot(1,1,1)
# Plot temperature
for i in range(sens+1):
    if ino[i]!=99:
        plot1.plot(range(minutes), RHtemp[ino[i]], linewidth=1.2, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
if campus!=99:
    num=11
    plot1.plot(range(minutes), temp150, linewidth=1.2, linestyle='--', color=plotcolmeso[0], label=legendlabelmeso[num])
    num=0
    plot1.plot(range(minutes), temp2m, linewidth=1.2, color=plotcolmeso[0], label=legendlabelmeso[num])   
    num=12
    plot1.plot(range(minutes), temp950, linewidth=1.2, linestyle='--', color=plotcolmeso[1], label=legendlabelmeso[num])
    num=1
    plot1.plot(range(minutes), temp10m, linewidth=1.2, color=plotcolmeso[1], label=legendlabelmeso[num])    

# strlabels are the minutes used as x axis labels (see set_xticklabels)
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
plot1.set_ylim([TRHmin,TRHmax])
plot1.set_yticks(np.arange(TRHmin,TRHmax+0.1,TRHinc))
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
plot1.set_ylabel(r"Temperature ($^{o}$C)",fontsize = 18)
plot1.text(1,TRHmax+TRHinc,"RH Sensor Temperature Comparison %s " % (date),fontsize=22,fontweight='bold')
plot1.legend(loc=2)
plot1.grid(which='both',axis='both',color='LightGrey',linestyle='dotted')

# Write average values:
if (minutes < 30):
    offset=10
else:
    offset=25

inc = (TRHmax-TRHmin)*0.09214/4.3
plot1.text(minutes-offset,TRHmax+4.3*inc,"Average Values:",horizontalalignment='left',fontsize=18,fontweight='bold')
plot1.text(minutes-offset,TRHmax+3.3*inc,"2m T = %5.2f $^{o}$C" % (avetemp2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,TRHmax+2.3*inc,"10m T = %5.2f $^{o}$C" % (avetemp10m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,TRHmax+1.3*inc,"2m RH = %5.2f " % (averh2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,TRHmax+0.3*inc,"10m RH = %5.2f " % (averh10m),horizontalalignment='left',fontsize=18,fontweight='normal')

plot1.text(minutes-5,TRHmax+3.3*inc,"2m wind = %5.2f m s$^{-1}$" % (avespeed2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,TRHmax+2.3*inc,"10m wind = %5.2f m s$^{-1}$" % (avespeed10m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,TRHmax+1.3*inc,"pressure = %7.2f mb" % (avepressure),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,TRHmax+0.3*inc,"radiation = %5.2f W m$^{-2}$" % (averadiation),horizontalalignment='left',fontsize=18,fontweight='normal')

# Add a right side y axis for Total Radiation.
if campus!=99:
    plot2 = plot1.twinx()
    plot2.plot(range(minutes), radiation, linewidth=1.0, linestyle='--', color='tomato', label="Total Radiation")
    plot2.set_ylim(radmin,radmax)
# Plot iMET pressure (it is always on the quad)
    a=1280/(presmax-presmin)
    b=1300-a*presmax
    plot2.plot(range(minutes), (presiMET[ipresFAST]*a + b), linewidth=1.0, linestyle='-', color='black', label="scaled iMET pressure")
    plot2.plot(range(minutes), (presiMET[ipresCHILI]*a + b), linewidth=1.0, linestyle='-', color='black')
    yticks=[]
    yticks=np.arange(radmin,radmax+0.1,radinc)
    plot2.get_yaxis().get_major_formatter().set_useOffset(False)
# To trim the margins
#tight_layout()
    plot2.set_yticks(yticks)
    for label in plot2.get_yticklabels():
        label.set_color('tomato')
        label.set_size(18)
    plot2.set_ylabel(r"Total Radiation (W m$^{-2}$)",fontsize = 18, color='tomato')
# put legend in upper right corner
    plot2.legend(loc=1)
# Write the plot to a file 
figure1.savefig(directory + "iMET-Tower-RHTempComparison-%s-1minave.png" % (date))
pp.savefig()
plt.close(figure1)
print 'one more'

## Plot RH
###########
figure2 = plt.figure(figsize = (25, 15))
plot1 = figure2.add_subplot(1,1,1)
for i in range(sens+1):
    if ino[i]!=99:
        plot1.plot(range(minutes), RHiMET[ino[i]], linewidth=1.0, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
        plot1.plot(range(minutes), RHadjust[ino[i]], linewidth=1.0, linestyle='--', color=plotcoliMET[ino[i]])
if campus!=99:
    num=2
    plot1.plot(range(minutes), rh2m, linewidth=1.2, color=plotcolmeso[0], label=legendlabelmeso[num])
    num=3
    plot1.plot(range(minutes), rh10m, linewidth=1.2, color=plotcolmeso[1], label=legendlabelmeso[num])

# strlabels are the minutes used as x axis labels (see set_xticklabels)
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
plot1.set_ylim([RHmin,RHmax])
plot1.set_yticks(np.arange(RHmin,RHmax+0.1,RHinc))
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
plot1.set_ylabel(r"Relative Humidity (%)",fontsize = 18)
plot1.text(1,RHmax+RHinc,"RH Comparison (dashed is adjusted RH) %s " % (date),fontsize=22,fontweight='bold')
plot1.legend(loc=2)

## Add a right side y axis for pressure (to indicate elevation of iMET ipres, which is on the quad).
plot2 = plot1.twinx()
#for i in range(sens+1):
#    if ino[i]==ipres:
#        plot2.plot(range(minutes), presiMET[ino[i]], linewidth=1.0, linestyle='--', color='tomato', label="iMET pressure")
#a=1280/(presmax-presmin)
#b=1300-a*presmax
plot2.plot(range(minutes), (presiMET[ipresFAST]), linewidth=1.0, linestyle='-', color='black', label="scaled iMET pressure")
plot2.plot(range(minutes), (presiMET[ipresCHILI]), linewidth=1.0, linestyle='-', color='black')
plot2.set_ylim([presmin,presmax])
yticks=[]
yticks=np.arange(presmin,presmax+0.1,presinc)
plot2.get_yaxis().get_major_formatter().set_useOffset(False)
plot2.set_yticks(yticks)
for label in plot2.get_yticklabels():
    label.set_color('black')
    label.set_size(18)
plot2.set_ylabel(r"Pressure (mb)",fontsize = 18, color='black')
# put legend in upper right corner
plot2.legend(loc=1)
# Write the plot to a file 
figure2.savefig(directory + "iMET-Tower-RHComparison-%s-1minave.png" % (date))
pp.savefig()
plt.close(figure2)
print 'and another'

## Plot wind speed and direction
################################
if campus!=99:
    figure3 = plt.figure(figsize = (25, 15))
    plot1 = figure3.add_subplot(1,1,1)

    num=4
    plot1.scatter(range(minutes), dir2m, linewidth=1.2, color=plotcolmeso[0], label=legendlabelmeso[num])
    num=5
    plot1.scatter(range(minutes), dir10m, linewidth=1.2, color=plotcolmeso[1], label=legendlabelmeso[num])

# strlabels are the minutes used as x axis labels (see set_xticklabels)
    plot1.set_xlim([0,minutes])
    plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
    plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)

    plot1.set_ylim([0.,360.])
    plot1.set_yticks(np.arange(0.,360.1,45.0))
# Make the y labels bigger.
    for label in plot1.get_yticklabels():
        label.set_size(18)
    plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
    plot1.set_ylabel(r"Wind Direction (degrees)",fontsize = 18)
# Write a blank title line, otherwise the figures are going to get squeezed together
    plot1.set_title("    " )
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
    plot1.text(1,380.0,"Wind Speed and Direction %s " % (date),fontsize=22,fontweight='bold')
#    plot1.text(-2,-20.0,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')

# Add a right side y axis for wind speed.
    plot2 = plot1.twinx()
    num=6
    plot2.plot(range(minutes), speed2m, linewidth=1.2, color=plotcolmeso[0], label=legendlabelmeso[num])
    num=7
    plot2.plot(range(minutes), speed10m, linewidth=1.2, color=plotcolmeso[1], label=legendlabelmeso[num])
# Plot 2m dewpoint
    plot2.plot(range(minutes), tdew2m, linewidth=1.2, color="fuchsia", label= "2m Dew Point Temperature")

    plot2.set_ylim([0.0,10.0])
    yticks=[]
    yticks=np.arange(0.0,10.1,1)
    plot2.get_yaxis().get_major_formatter().set_useOffset(False)
# To trim the margins
#tight_layout()
    plot2.set_yticks(yticks)
    for label in plot2.get_yticklabels():
        label.set_color('black')
        label.set_size(18)
    plot2.set_ylabel(r"Wind Speed (m s$^{-1}$) and Elevation (m)",fontsize = 18, color='black')

# put legend in upper left corner
    plot1.legend(loc=2)
# put legend in upper right corner
    plot2.legend(loc=1)

# To pull out the plot box so that the margins are narrow; this does, however, remove text outside the plotting area such as titles.
#plt.tight_layout()

# Write the plot to a file 
    figure3.savefig(directory + "iMET-Tower-WindComparison-%s-1minave.png" % (date))
    pp.savefig()
    plt.close(figure3)
    print 'lots of plots here'

### Plot weather station and iMET pressures
###########################################
figure4 = plt.figure(figsize = (25, 15))
plot1 = figure4.add_subplot(1,1,1)
for i in range(sens+1):
    if ino[i]!=99:
        plot1.plot(range(minutes), presiMET[ino[i]], linewidth=1.2, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
if campus!=99:
    num=8
    plot1.plot(range(minutes), pressure1, linewidth=1.2, color=plotcolmeso[0], label=legendlabelmeso[num])
    num=9
    plot1.plot(range(minutes), pressure2, linewidth=1.2, color=plotcolmeso[1], label=legendlabelmeso[num])
# strlabels are the minutes used as x axis labels (see set_xticklabels)
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
plot1.set_ylim([presmin,presmax])
plot1.set_yticks(np.arange(presmin,presmax+0.1,presinc))
plot1.get_yaxis().get_major_formatter().set_useOffset(False)
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
plot1.set_ylabel(r"Pressure (mb)",fontsize = 18)
# Write a blank title line, otherwise the figures are going to get squeezed together
plot1.set_title("    " )
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
plot1.text(1,presmax+presinc/2.,"Pressure Comparison %s " % (date),fontsize=22,fontweight='bold')
#plot1.text(-2,presmin-presinc/2.,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figure4.savefig(directory + "iMET-Tower-PressureComparison-%s-1minave.png" % (date))
pp.savefig()
plt.close(figure4)
print 'Pressure is done'

### Plot weather station and iMET latitudes
###########################################
figure5 = plt.figure(figsize = (25, 15))
plot1 = figure5.add_subplot(1,1,1)
for i in range(sens+1):
    if ino[i]!=99:
        plot1.plot(range(minutes), latiMET[ino[i]], linewidth=1.2, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
if campus!=99:
    num=10
    plot1.plot(range(minutes), lattow, linewidth=1.2, color=plotcolmeso[1], label=legendlabelmeso[num])

# strlabels are the minutes used as x axis labels (see set_xticklabels)
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)

plot1.set_ylim([latmin,latmax])
plot1.set_yticks(np.arange(latmin,latmax+0.00001,latinc))
plot1.get_yaxis().get_major_formatter().set_useOffset(False)
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
plot1.set_ylabel(r"Latitude ($^{o}N$)",fontsize = 18)
# Write a blank title line, otherwise the figures are going to get squeezed together
plot1.set_title("    " )
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
inc = (latmax-latmin)*0.09214/(4.3)
plot1.text(1,latmax+2*inc,"Latitude Comparison %s " % (date),fontsize=22,fontweight='bold')
#plot1.text(-2,latmin-2*latinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')

# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
plot1 = figure5.add_subplot(1,1,1)
figure5.savefig(directory + "iMET-Tower-LatitudeComparison-%s-1minave.png" % (date))
pp.savefig()
plt.close(figure5)
print 'Latitude. oh yea'
               
### Plot Temperature difference compared to 2m tower sensor
###########################################################
figureTdiff = plt.figure(figsize = (25, 15))
plot1 = figureTdiff.add_subplot(1,1,1)
Tdiffmin = 10000
Tdiffmax = -10000
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=tempiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((temp2m-plotarray)/temp2m)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (temp2m-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])
            m = np.nanmin(temp2m-plotarray)
            if m < Tdiffmin:
                Tdiffmin = m
            m = np.nanmax(temp2m-plotarray)
            if m > Tdiffmax:
                Tdiffmax = m

Tdiffmin = -np.ceil(-Tdiffmin)
Tdiffmax = np.ceil(Tdiffmax)
plot1.plot(range(minutes), minerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[0]) 
plot1.plot(range(minutes), maxerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[0]) 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[0]) 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffinc=1
plot1.set_ylim([Tdiffmin,Tdiffmax])
plot1.set_yticks(np.arange(Tdiffmin,Tdiffmax+0.00001,Tdiffinc))
plot1.get_yaxis().get_major_formatter().set_useOffset(False)
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
plot1.set_ylabel(r"Temperature Difference ($^{o}C$)",fontsize = 18)
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
inc = (Tdiffmax-Tdiffmin)*0.09214/4.3
plot1.text(1,Tdiffmax+2*inc,"Temperature difference with 2m T %s " % (date),fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureTdiff.savefig(directory + "2mTempDiffError-%s-1minave.png" % (date))
pp.savefig()
plt.close(figureTdiff)
print 'Temp diff'
        
### Plot Temperature difference compared to 10m tower sensor
############################################################
figureTdiff = plt.figure(figsize = (25, 15))
plot1 = figureTdiff.add_subplot(1,1,1)
Tdiffmin = 10000
Tdiffmax = -10000
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=tempiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((temp10m-plotarray)/temp10m)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (temp10m-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num]) 
            m = np.nanmin(temp10m-plotarray)
            if m < Tdiffmin:
                Tdiffmin = m
            m = np.nanmax(temp10m-plotarray)
            if m > Tdiffmax:
                Tdiffmax = m

Tdiffmin = -np.ceil(-Tdiffmin)
Tdiffmax = np.ceil(Tdiffmax)
plot1.plot(range(minutes), minerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[1]) 
plot1.plot(range(minutes), maxerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[1]) 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[1]) 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffinc=1
plot1.set_ylim([Tdiffmin,Tdiffmax])
plot1.set_yticks(np.arange(Tdiffmin,Tdiffmax+0.00001,Tdiffinc))
plot1.get_yaxis().get_major_formatter().set_useOffset(False)
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
plot1.set_ylabel(r"Temperature Difference ($^{o}C$)",fontsize = 18)
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
plot1.text(1,Tdiffmax+2*inc,"Temperature difference with 10m T %s " % (date),fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureTdiff.savefig(directory + "10mTempDiffError-%s-1minave.png" % (date))
pp.savefig()
plt.close(figureTdiff)
print 'Temp diff.....10 meters'
RHdiffmin = 10000
RHdiffmax = -10000
### Plot RH difference compared to 2m tower sensor
##################################################
figureRHdiff = plt.figure(figsize = (25, 15))
plot1 = figureRHdiff.add_subplot(1,1,1)
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=RHiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((rh2m-plotarray)/rh2m)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (rh2m-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])
            m = np.nanmin(rh2m-plotarray)
            if m < RHdiffmin:
                RHdiffmin = m
            m = np.nanmax(rh2m-plotarray)
            if m > RHdiffmax:
                RHdiffmax = m

RHdiffmin = -np.ceil(-RHdiffmin)
RHdiffmax = np.ceil(RHdiffmax)
plot1.plot(range(minutes), minRHerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[2]) 
plot1.plot(range(minutes), maxRHerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[2]) 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[2])
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
RHdiffinc=np.round(0.2*(RHdiffmax-RHdiffmin)/7,1)
plot1.set_ylim([RHdiffmin,RHdiffmax])
plot1.set_yticks(np.arange(RHdiffmin,RHdiffmax+0.00001,RHdiffinc))
plot1.get_yaxis().get_major_formatter().set_useOffset(False)
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
plot1.set_ylabel(r"RH Difference (%)",fontsize = 18)
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
inc = (RHmax-RHmin)*0.09214/4.3
plot1.text(1,RHdiffmax+inc,"RH difference with 2m RH %s " % (date),fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureRHdiff.savefig(directory + "2mRHDiffError-%s-1minave.png" % (date))
pp.savefig()
plt.close(figureRHdiff)
print 'RH @ 2m'
        
### Plot RH difference compared to 10m tower sensor
###################################################
figureRHdiff = plt.figure(figsize = (25, 15))
plot1 = figureRHdiff.add_subplot(1,1,1)
RHdiffmin = 10000
RHdiffmax = -10000
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=RHiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((rh10m-plotarray)/rh10m)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num]) 
            plot1.plot(range(minutes), (rh10m-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            m = np.nanmin(rh10m-plotarray)
            if m < RHdiffmin:
                RHdiffmin = m
            m = np.nanmax(rh10m-plotarray)
            if m > RHdiffmax:
                RHdiffmax = m

RHdiffmin = -np.ceil(-RHdiffmin)
RHdiffmax = np.ceil(RHdiffmax)
plot1.plot(range(minutes), minRHerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[3]) 
plot1.plot(range(minutes), maxRHerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[3]) 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[3]) 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
RHdiffinc=np.round(0.2*(RHdiffmax-RHdiffmin)/7,1)
plot1.set_ylim([RHdiffmin,RHdiffmax])
plot1.set_yticks(np.arange(RHdiffmin,RHdiffmax+0.00001,RHdiffinc))
plot1.get_yaxis().get_major_formatter().set_useOffset(False)
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
plot1.set_ylabel(r"RH Difference (%)",fontsize = 18)
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
inc = (RHmax-TRHmin)*0.09214/4.3
plot1.text(1,RHdiffmax+inc,"RH difference with 10m RH %s " % (date),fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureRHdiff.savefig(directory + "10mRHDiffError-%s-1minave.png" % (date))
pp.savefig()
plt.close(figureRHdiff)
print 'RH diff'

##Plot dew point temperature data
#################################    
figure6 = plt.figure(figsize = (25, 15))
plot1 = figure6.add_subplot(1,1,1)
# Plot temperature
for i in range(sens+1):
    if ino[i]!=99:
        plot1.plot(range(minutes), tdewiMET[ino[i]], linewidth=1.2, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
if campus!=99:
    num=0
    plot1.plot(range(minutes), tdew2m, linewidth=1.2, color=plotcolmeso[0], label=legendlabelmeso[num])   
    num=1
    plot1.plot(range(minutes), tdew10m, linewidth=1.2, color=plotcolmeso[1], label=legendlabelmeso[num])    

# strlabels are the minutes used as x axis labels (see set_xticklabels)
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
plot1.set_ylim([Tdmin,Tdmax])
plot1.set_yticks(np.arange(Tdmin,Tdmax+0.1,Tdinc))
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
plot1.set_ylabel(r"Dew Point Temperature $^{o}C$",fontsize = 18)
plot1.text(1,Tdmax+Tdinc,"Dew Point Temperature Comparison %s " % (date),fontsize=22,fontweight='bold')
plot1.legend(loc=2)

# Add a right side y axis for Total Radiation.
if campus!=99:
    plot2 = plot1.twinx()
    plot2.plot(range(minutes), radiation, linewidth=1.0, linestyle='--', color='tomato', label="Total Radiation")
    plot2.set_ylim(radmin,radmax)
# Plot pressure for one iMETs on each quad
    a=1280/(presmax-presmin)
    b=1300-a*presmax
    plot2.plot(range(minutes), (presiMET[ipresFAST]*a + b), linewidth=1.0, linestyle='-', color='black', label="scaled iMET pressure")
    plot2.plot(range(minutes), (presiMET[ipresCHILI]*a + b), linewidth=1.0, linestyle='-', color='black', label="scaled iMET pressure")
    yticks=[]
    yticks=np.arange(radmin,radmax+0.1,radinc)
    plot2.get_yaxis().get_major_formatter().set_useOffset(False)
# To trim the margins
#tight_layout()
    plot2.set_yticks(yticks)
    for label in plot2.get_yticklabels():
        label.set_color('tomato')
        label.set_size(18)
    plot2.set_ylabel(r"Total Radiation (W m$^{-2}$)",fontsize = 18, color='tomato')
# put legend in upper right corner
    plot2.legend(loc=1)
# Write the plot to a file 
figure6.savefig(directory + "iMET-Tower-DewPointComparison-%s-1minave.png" % (date))
pp.savefig()
plt.close(figure6)
print 'So many plots'

### Plot Temperature difference compared to the averaged iMET temperature
#########################################################################
figureTdiff2 = plt.figure(figsize = (25, 15))
plot1 = figureTdiff2.add_subplot(1,1,1)
Tdiffmin = 10000
Tdiffmax = -10000
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=tempiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((tempave-plotarray)/tempave)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (tempave-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])
            m = np.nanmin(tempave-plotarray)
            if m < Tdiffmin:
                Tdiffmin = m
            m = np.nanmax(tempave-plotarray)
            if m > Tdiffmax:
                Tdiffmax = m
            
Tdiffmin = -np.ceil(-Tdiffmin)
Tdiffmax = np.ceil(Tdiffmax)
plot1.plot(range(minutes), minerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), maxerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black") 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffinc=np.round(0.2*(Tdiffmax-Tdiffmin)/7,1)
plot1.set_ylim([Tdiffmin,Tdiffmax])
plot1.set_yticks(np.arange(Tdiffmin,Tdiffmax+0.00001,Tdiffinc))
plot1.get_yaxis().get_major_formatter().set_useOffset(False)
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
plot1.set_ylabel(r"Temperature Difference ($^{o}C$)",fontsize = 18)
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
inc = (Tdiffmax-Tdiffmin)*0.09214/4.3
plot1.text(1,Tdiffmax+1.5*inc,"Temperature difference with average iMET T %s " % (date),fontsize=22,fontweight='bold')
plot1.text(1,Tdiffmax+0.5*inc,"NOTE: iMET average comparison not meaningful for 10m flights because 2m iMETs included in average.",fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureTdiff2.savefig(directory + "iMETaveTempDiffError-%s-1minave.png" % (date))
pp.savefig()
plt.close(figureTdiff2)
print 'Some error'
 
### Plot RH difference compared to the averaged iMET RH
#######################################################
figureRHdiff = plt.figure(figsize = (25, 15))
plot1 = figureRHdiff.add_subplot(1,1,1)
Tdiffmin = 10000
Tdiffmax = -10000
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=RHiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((RHave-plotarray)/RHave)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (RHave-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num]) 
            m = np.nanmin(RHave-plotarray)
            if m < Tdiffmin:
                Tdiffmin = m
            m = np.nanmax(RHave-plotarray)
            if m > Tdiffmax:
                Tdiffmax = m

Tdiffmin = -np.ceil(-Tdiffmin)
Tdiffmax = np.ceil(Tdiffmax)
plot1.plot(range(minutes), minRHerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), maxRHerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black") 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffinc=np.round(0.2*(Tdiffmax-Tdiffmin)/7,1)
plot1.set_ylim([Tdiffmin,Tdiffmax])
plot1.set_yticks(np.arange(Tdiffmin,Tdiffmax+0.00001,Tdiffinc))
plot1.get_yaxis().get_major_formatter().set_useOffset(False)
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
plot1.set_ylabel(r"RH Difference (%)",fontsize = 18)
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
inc = (Tdiffmax-Tdiffmin)*0.09214/4.3
plot1.text(1,Tdiffmax+1.5*inc,"RH difference with average iMET RH, %s " % (date),fontsize=22,fontweight='bold')
plot1.text(1,Tdiffmax+0.5*inc,"NOTE: iMET average comparison not meaningful for 10m flights because 2m iMETs included in average.",fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureRHdiff.savefig(directory + "iMETaveRHDiffError-%s-1minave.png" % (date))
pp.savefig()
plt.close(figureRHdiff)
print 'Diff error?'

### Plot pressure difference compared to the averaged iMET pressure
###################################################################
figurepdiff = plt.figure(figsize = (25, 15))
plot1 = figurepdiff.add_subplot(1,1,1)
Tdiffmin = 10000
Tdiffmax = -10000
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=presiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((presave-plotarray)/presave)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (presave-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            m = np.nanmin(presave-plotarray)
            if m < Tdiffmin:
                Tdiffmin = m
            m = np.nanmax(presave-plotarray)
            if m > Tdiffmax:
                Tdiffmax = m

Tdiffmin = -np.ceil(-Tdiffmin)
Tdiffmax = np.ceil(Tdiffmax)
plot1.plot(range(minutes), minperror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), maxperror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black") 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffinc = np.ceil((Tdiffmax-Tdiffmin)/10)
plot1.set_ylim([Tdiffmin,Tdiffmax])
plot1.set_yticks(np.arange(Tdiffmin,Tdiffmax+0.00001,Tdiffinc))
plot1.get_yaxis().get_major_formatter().set_useOffset(False)
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
plot1.set_ylabel(r"Pressure Difference (mb)",fontsize = 18)
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
inc = (Tdiffmax-Tdiffmin)*0.09214/4.3
plot1.text(1,Tdiffmax+1.5*inc,"Pressure difference with average iMET pressure, %s " % (date),fontsize=22,fontweight='bold')
plot1.text(1,Tdiffmax+0.5*inc,"NOTE: iMET average comparison not meaningful for 10m flights because 2m iMETs included in average.",fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figurepdiff.savefig(directory + "iMETavePresDiffError-%s-1minave.png" % (date))
pp.savefig()
plt.close(figurepdiff)
print 'Don''t even know'

### Plot Dew Point Temperature differences compared to the averaged iMET dew point temperature
##############################################################################################
figureTdiff3 = plt.figure(figsize = (25, 15))
plot1 = figureTdiff3.add_subplot(1,1,1)
Tdiffmin = 10000
Tdiffmax = -10000
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=tdewiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), (tdewave-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (tdewave-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])
            m = np.nanmin(tdewave-plotarray)
            if m < Tdiffmin:
                Tdiffmin = m
            m = np.nanmax(tdewave-plotarray)
            if m > Tdiffmax:
                Tdiffmax = m

Tdiffmin = -np.ceil(-Tdiffmin)
Tdiffmax = np.ceil(Tdiffmax)
plot1.plot(range(minutes), mindewerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), maxdewerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black") 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffinc=np.round(0.2*(Tdiffmax-Tdiffmin)/7,1)
plot1.set_ylim([Tdiffmin,Tdiffmax])
plot1.set_yticks(np.arange(Tdiffmin,Tdiffmax+0.00001,Tdiffinc))
plot1.get_yaxis().get_major_formatter().set_useOffset(False)
# Make the y labels bigger.
for label in plot1.get_yticklabels():
    label.set_size(18)
plot1.set_xlabel("Time (CST)",fontsize = 18)
# The r enables Latex formatting, the $ signs enable math mode and allow exponentials
plot1.set_ylabel(r"Dew Point Temperature Difference ($^{o}C$)",fontsize = 18)
# the first 2 numbers are the x and y location, respectively. Numers are relative to the x and y values 
# (i.e. for x this is the data array values) on the figure!
inc = (Tdiffmax-Tdiffmin)*0.09214/4.3
plot1.text(1,Tdiffmax+1.5*inc,"Dew Point Temperature difference with average iMET Tdew %s " % (date),fontsize=22,fontweight='bold')
plot1.text(1,Tdiffmax+0.5*inc,"NOTE: iMET average comparison not meaningful for 10m flights because 2m iMETs included in average.",fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureTdiff3.savefig(directory + "iMETaveTdewDiffError-%s-1minave.png" % (date))
pp.savefig()
plt.close(figureTdiff3)
print 'Wow'

# Write out Temperature values to check
print "Time   Mesonet     iMET3     iMET5     iMET7     iMET9     iMET10    iMET11    iMET12    iMET13    iMET15    iMET16     iMET17    iMET18    iMET19    iMET20    iMET21    iMET22"
for i in range(minutes):
    print timelabel[i].rjust(3),"%9.2f" %(temp2m[i]),"%9.2f" %(tempiMET[3,i]),"%9.2f" %(tempiMET[5,i]),"%9.2f" %(tempiMET[7,i]),"%9.2f" %(tempiMET[9,i]),"%9.2f" %(tempiMET[10,i]),"%9.2f" %(tempiMET[11,i]),"%9.2f" %(tempiMET[12,i]),"%9.2f" %(tempiMET[13,i]),"%9.2f" %(tempiMET[15,i]),"%9.2f" %(tempiMET[16,i]),"%9.2f" %(tempiMET[17,i]),"%9.2f" %(tempiMET[18,i]),"%9.2f" %(tempiMET[19,i]),"%9.2f" %(tempiMET[20,i]),"%9.2f" %(tempiMET[21,i]),"%9.2f" %(tempiMET[22,i])

print "Write to JMP files"

# Write to 2m JMP output file
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# First wipe out non-airborne data for iMETs located on quadcopters
wipe = np.ndarray((minutes),dtype=int)
wipe = np.full((minutes),99,dtype=int)
for j in range(len(timelabel)): 
    hour=float(timelabel[j].split(':')[0])
    minute=float(timelabel[j].split(':')[1])
    time=hour+minute/60. 
    for t in range(flights2m):
        starthour=float(start2mflight[t].split(':')[0])
        startmin=float(start2mflight[t].split(':')[1])
        starttime=starthour+startmin/60.
        endhour=float(end2mflight[t].split(':')[0])
        endmin=float(end2mflight[t].split(':')[1])
        endtime=endhour+endmin/60.
        if(starttime<=time and time<=endtime):
            wipe[j]=0 

Tlist = []
RHlist =[]
loclist = []
RHalist = []
RHTlist = []
for i in range(sensor1,sens+1):
    Tlist.append('TiMET'+str(i))
    RHlist.append('RHiMET'+str(i))
    RHalist.append('RHadjust'+str(i))
    RHTlist.append('RHtemp'+str(i))
    loclist.append('location'+str(i))

if (flights2m!=0):      
# Open the output JMP files and write title line
    name='2mflight-'+date
    fname = "%s.dat" % (name)
    fout2m=open(directory+fname,"w")  
    fout2m.write("year    month   day  hour  min      T2m    T1.5m   RH2m  RH10m   radiation  2mwindspeed  2mwinddir")
    for i in range(len(RHlist)):
         fout2m.write(Tlist[i].rjust(10))
    for i in range(len(RHlist)):
         fout2m.write(RHlist[i].rjust(10))     
    for i in range(len(RHlist)):
         fout2m.write(RHalist[i].rjust(12)) 
    for i in range(len(RHTlist)):
         fout2m.write(RHTlist[i].rjust(10)) 
    for i in range(len(RHlist)):
         fout2m.write(loclist[i].rjust(20))
    fout2m.write("\n")
    year=date[-4:]
    month=date[-7:-4]
    if(len(date)==8):
        day=str(date[0])
    if(len(date)==9):
        day=str(date[0:2])
# The first and last minute of the iMETs are almost always incomplete, therefore,
# they contain averages that were calculate using < 60 seconds.
# So they will not be used in the JMP analysis. 
# From the iMETs on the quad, data will only be used once the quad is airborne and at altitude; these times 
# are read off the charts and set in UserSettings.py
    for j in range(1,minutes-1):
        if(wipe[j]==0):
            hour=timelabel[j].split(':')[0]
            minute=timelabel[j].split(':')[1]
            fout2m.write(year.ljust(8))
            fout2m.write(month.ljust(8))
            fout2m.write(day.ljust(6))
            fout2m.write(hour.ljust(6))
            fout2m.write(minute.ljust(6))
            if(np.isnan(temp2m[j])):
                temp2m[j]=999.99
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(temp2m[j]))
            if(np.isnan(temp150[j])):
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(temp150[j]))                
            if(np.isnan(rh2m[j])):
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(rh2m[j]))
            if(np.isnan(rh10m[j])):
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(rh10m[j]))                 
            if(np.isnan(radiation[j])):
                fout2m.write("%12.2f" %(999.99))
            else:
                fout2m.write("%12.2f" %(radiation[j]))
            if(np.isnan(speed2m[j])):
                fout2m.write("%13.2f" %(999.99))
            else:
                fout2m.write("%13.2f" %(speed2m[j]))
            if(np.isnan(dir2m[j])):
                fout2m.write("%11.2f" %(999.99))
            else:
                fout2m.write("%11.2f" %(dir2m[j]))            
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(tempiMET[i,j])):
                    fout2m.write("%10.2f" %(999.99))
                else: 
                    fout2m.write("%10.2f" %(tempiMET[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHiMET[i,j])):
                    fout2m.write("%10.2f" %(999.99))
                else: 
                    fout2m.write("%10.2f" %(RHiMET[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHadjust[i,j])):
                    fout2m.write("%12.2f" %(999.99))
                else: 
                    fout2m.write("%12.2f" %(RHadjust[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHtemp[i,j])):
                    fout2m.write("%10.2f" %(999.99))
                else: 
                    fout2m.write("%10.2f" %(RHtemp[i,j]))                    
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or len(iMETname[i])==0):
                    fout2m.write("%20.2f" %(999.99))
                else: 
                    fout2m.write(iMETname[i].rjust(20))
            fout2m.write(str("\n"))
    fout2m.close()  


# Write to 10m JMP output file
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# First wipe out non-airborne data for iMETs located on quadcopters
wipe = np.ndarray((minutes),dtype=int)
wipe = np.full((minutes),99,dtype=int)
for j in range(len(timelabel)): 
    hour=float(timelabel[j].split(':')[0])
    minute=float(timelabel[j].split(':')[1])
    time=hour+minute/60. 
    for t in range(flights10m):
        starthour=float(start10mflight[t].split(':')[0])
        startmin=float(start10mflight[t].split(':')[1])
        starttime=starthour+startmin/60.
        endhour=float(end10mflight[t].split(':')[0])
        endmin=float(end10mflight[t].split(':')[1])
        endtime=endhour+endmin/60.
        if(starttime<=time and time<=endtime):
            wipe[j]=0 

if (flights10m!=0):      
# Open the output JMP files and write title line
    name='10mflight-'+date
    fname = "%s.dat" % (name)
    fout10m=open(directory+fname,"w")  
    fout10m.write("year    month   day  hour  min      T2m    T1.5m  RH2m  RH10m   radiation  2mwindspeed  2mwinddir")
    for i in range(len(RHlist)):
         fout10m.write(Tlist[i].rjust(10))
    for i in range(len(RHlist)):
         fout10m.write(RHlist[i].rjust(10))  
    for i in range(len(RHlist)):
         fout10m.write(RHalist[i].rjust(12))  
    for i in range(len(RHlist)):
         fout10m.write(RHTlist[i].rjust(10))   
    for i in range(len(RHlist)):
         fout10m.write(loclist[i].rjust(20))
    fout10m.write("\n")
    year=date[-4:]
    month=date[-7:-4]
    if(len(date)==8):
        day=str(date[0])
    if(len(date)==9):
        day=str(date[0:2])
# The first and last minute of the iMETs are almost always incomplete, therefore,
# they contain averages that were calculate using < 60 seconds.
# So they will not be used in the JMP analysis. 
# From the iMETs on the quad, data will only be used once the quad is airborne and at altitude; these times 
# are read off the charts and set in UserSettings.py
    for j in range(1,minutes-1):
        if(wipe[j]==0):
            hour=timelabel[j].split(':')[0]
            minute=timelabel[j].split(':')[1]
            fout10m.write(year.ljust(8))
            fout10m.write(month.ljust(8))
            fout10m.write(day.ljust(6))
            fout10m.write(hour.ljust(6))
            fout10m.write(minute.ljust(6))
            if(np.isnan(temp2m[j])):
                temp2m[j]=999.99
                fout10m.write("%7.2f" %(999.99))
            else:
                fout10m.write("%7.2f" %(temp2m[j]))
            if(np.isnan(temp150[j])):
                fout10m.write("%7.2f" %(999.99))
            else:
                fout10m.write("%7.2f" %(temp150[j]))                
            if(np.isnan(rh2m[j])):
                fout10m.write("%7.2f" %(999.99))
            else:
                fout10m.write("%7.2f" %(rh2m[j]))
            if(np.isnan(rh10m[j])):
                fout10m.write("%7.2f" %(999.99))
            else:
                fout10m.write("%7.2f" %(rh10m[j]))                 
            if(np.isnan(radiation[j])):
                fout10m.write("%12.2f" %(999.99))
            else:
                fout10m.write("%12.2f" %(radiation[j]))
            if(np.isnan(speed2m[j])):
                fout10m.write("%13.2f" %(999.99))
            else:
                fout10m.write("%13.2f" %(speed2m[j]))
            if(np.isnan(dir2m[j])):
                fout10m.write("%11.2f" %(999.99))
            else:
                fout10m.write("%11.2f" %(dir2m[j]))            
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(tempiMET[i,j])):
                    fout10m.write("%10.2f" %(999.99))
                else: 
                    fout10m.write("%10.2f" %(tempiMET[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHiMET[i,j])):
                    fout10m.write("%10.2f" %(999.99))
                else: 
                    fout10m.write("%10.2f" %(RHiMET[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHadjust[i,j])):
                    fout10m.write("%12.2f" %(999.99))
                else: 
                    fout10m.write("%12.2f" %(RHadjust[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHtemp[i,j])):
                    fout10m.write("%10.2f" %(999.99))
                else: 
                    fout10m.write("%10.2f" %(RHtemp[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or len(iMETname[i])==0):
                    fout10m.write("%20.2f" %(999.99))
                else: 
                    fout10m.write(iMETname[i].rjust(20))
            fout10m.write(str("\n"))
    fout10m.close()   

# Write to soundings JMP output file
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# First wipe out non-airborne data between flights
wipe = np.ndarray((minutes),dtype=int)
wipe = np.full((minutes),99,dtype=int)
for j in range(len(timelabel)): 
    hour=float(timelabel[j].split(':')[0])
    minute=float(timelabel[j].split(':')[1])
    time=hour+minute/60. 
    for t in range(soundings):
        starthour=float(startsounding[t].split(':')[0])
        startmin=float(startsounding[t].split(':')[1])
        starttime=starthour+startmin/60.
        endhour=float(endsounding[t].split(':')[0])
        endmin=float(endsounding[t].split(':')[1])
        endtime=endhour+endmin/60.
        if(starttime<=time and time<=endtime):
            wipe[j]=0 


if (soundings!=0):      
# Open the output JMP files and write title line
    name='soundings-'+date
    fname = "%s.dat" % (name)
    fout2m=open(directory + fname,"w")  
    fout2m.write("year    month   day  hour  min      T2m    T1.5m   RH2m  RH10m   radiation  2mwindspeed  2mwinddir")
    for i in range(len(RHlist)):
         fout2m.write(Tlist[i].rjust(10))
    for i in range(len(RHlist)):
         fout2m.write(RHlist[i].rjust(10))   
    for i in range(len(RHlist)):
         fout2m.write(RHalist[i].rjust(12)) 
    for i in range(len(RHlist)):
         fout2m.write(RHTlist[i].rjust(10)) 
    for i in range(len(RHlist)):
         fout2m.write(loclist[i].rjust(20))
    fout2m.write("\n")
    year=date[-4:]
    month=date[-7:-4]
    if(len(date)==8):
        day=str(date[0])
    if(len(date)==9):
        day=str(date[0:2])
# The first and last minute of the iMETs are almost always incomplete, therefore,
# they contain averages that were calculate using < 60 seconds.
# So they will not be used in the JMP analysis. 
# From the iMETs on the quad, data will only be used once the quad is airborne and at altitude; these times 
# are read off the charts and set in UserSettings.py
    for j in range(1,minutes-1):
        if(wipe[j]==0):
            hour=timelabel[j].split(':')[0]
            minute=timelabel[j].split(':')[1]
            fout2m.write(year.ljust(8))
            fout2m.write(month.ljust(8))
            fout2m.write(day.ljust(6))
            fout2m.write(hour.ljust(6))
            fout2m.write(minute.ljust(6))
            if(np.isnan(temp2m[j])):
                temp2m[j]=999.99
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(temp2m[j]))
            if(np.isnan(temp150[j])):
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(temp150[j]))                
            if(np.isnan(rh2m[j])):
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(rh2m[j]))
            if(np.isnan(rh10m[j])):
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(rh10m[j]))                 
            if(np.isnan(radiation[j])):
                fout2m.write("%12.2f" %(999.99))
            else:
                fout2m.write("%12.2f" %(radiation[j]))
            if(np.isnan(speed2m[j])):
                fout2m.write("%13.2f" %(999.99))
            else:
                fout2m.write("%13.2f" %(speed2m[j]))
            if(np.isnan(dir2m[j])):
                fout2m.write("%11.2f" %(999.99))
            else:
                fout2m.write("%11.2f" %(dir2m[j]))            
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(tempiMET[i,j])):
                    fout2m.write("%10.2f" %(999.99))
                else: 
                    fout2m.write("%10.2f" %(tempiMET[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHiMET[i,j])):
                    fout2m.write("%10.2f" %(999.99))
                else: 
                    fout2m.write("%10.2f" %(RHiMET[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHadjust[i,j])):
                    fout2m.write("%12.2f" %(999.99))
                else: 
                    fout2m.write("%12.2f" %(RHadjust[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHtemp[i,j])):
                    fout2m.write("%10.2f" %(999.99))
                else: 
                    fout2m.write("%10.2f" %(RHtemp[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or len(iMETname[i])==0):
                    fout2m.write("%20.2f" %(999.99))
                else: 
                    fout2m.write(iMETname[i].rjust(20))
            fout2m.write(str("\n"))
    fout2m.close()   
    
# Write to twer JMP output file
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# First wipe out non-airborne data between flights
wipe = np.ndarray((minutes),dtype=int)
wipe = np.full((minutes),99,dtype=int)
for j in range(len(timelabel)): 
    hour=float(timelabel[j].split(':')[0])
    minute=float(timelabel[j].split(':')[1])
    time=hour+minute/60. 
    starthour=float(starttower.split(':')[0])
    startmin=float(starttower.split(':')[1])
    starttime=starthour+startmin/60.
    endhour=float(endtower.split(':')[0])
    endmin=float(endtower.split(':')[1])
    endtime=endhour+endmin/60.
    if(starttime<=time and time<=endtime):
        wipe[j]=0 

if (towertest!=0):      
# Open the output JMP files and write title line
    name='tower-'+date
    fname = "%s.dat" % (name)
    fout2m=open(directory + fname,"w")  
    fout2m.write("year    month   day  hour  min      T2m    T1.5m   RH2m  RH10m   radiation  2mwindspeed  2mwinddir")
    for i in range(len(RHlist)):
         fout2m.write(Tlist[i].rjust(10))
    for i in range(len(RHlist)):
         fout2m.write(RHlist[i].rjust(10))    
    for i in range(len(RHlist)):
         fout2m.write(RHalist[i].rjust(12)) 
    for i in range(len(RHlist)):
         fout2m.write(RHTlist[i].rjust(10))  
    for i in range(len(RHlist)):
         fout2m.write(loclist[i].rjust(20))
    fout2m.write("\n")
    year=date[-4:]
    month=date[-7:-4]
    if(len(date)==8):
        day=str(date[0])
    if(len(date)==9):
        day=str(date[0:2])
# The first and last minute of the iMETs are almost always incomplete, therefore,
# they contain averages that were calculate using < 60 seconds.
# So they will not be used in the JMP analysis. 
# From the iMETs on the quad, data will only be used once the quad is airborne and at altitude; these times 
# are read off the charts and set in UserSettings.py
    for j in range(1,minutes-1):
        if(wipe[j]==0):
            hour=timelabel[j].split(':')[0]
            minute=timelabel[j].split(':')[1]
            fout2m.write(year.ljust(8))
            fout2m.write(month.ljust(8))
            fout2m.write(day.ljust(6))
            fout2m.write(hour.ljust(6))
            fout2m.write(minute.ljust(6))
            if(np.isnan(temp2m[j])):
                temp2m[j]=999.99
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(temp2m[j]))
            if(np.isnan(temp150[j])):
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(temp150[j]))                
            if(np.isnan(rh2m[j])):
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(rh2m[j]))
            if(np.isnan(rh10m[j])):
                fout2m.write("%7.2f" %(999.99))
            else:
                fout2m.write("%7.2f" %(rh10m[j]))                                               
            if(np.isnan(radiation[j])):
                fout2m.write("%12.2f" %(999.99))
            else:
                fout2m.write("%12.2f" %(radiation[j]))
            if(np.isnan(speed2m[j])):
                fout2m.write("%13.2f" %(999.99))
            else:
                fout2m.write("%13.2f" %(speed2m[j]))
            if(np.isnan(dir2m[j])):
                fout2m.write("%11.2f" %(999.99))
            else:
                fout2m.write("%11.2f" %(dir2m[j]))            
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(tempiMET[i,j])):
                    fout2m.write("%10.2f" %(999.99))
                else: 
                    fout2m.write("%10.2f" %(tempiMET[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHiMET[i,j])):
                    fout2m.write("%10.2f" %(999.99))
                else: 
                    fout2m.write("%10.2f" %(RHiMET[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHadjust[i,j])):
                    fout2m.write("%12.2f" %(999.99))
                else: 
                    fout2m.write("%12.2f" %(RHadjust[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or np.isnan(RHtemp[i,j])):
                    fout2m.write("%10.2f" %(999.99))
                else: 
                    fout2m.write("%10.2f" %(RHtemp[i,j]))
            for i in range(sensor1,sens+1):
                if(ino[i]==99 or len(iMETname[i])==0):
                    fout2m.write("%20.2f" %(999.99))
                else: 
                    fout2m.write(iMETname[i].rjust(20))
            fout2m.write(str("\n"))
    fout2m.close()   

print 'and fin'
pp.close() #make one single pdf for plotting

