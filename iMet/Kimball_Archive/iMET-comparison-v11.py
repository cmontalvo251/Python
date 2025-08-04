import csv
import numpy as np
import matplotlib.pyplot as plt
import math
#from pylab import *
import matplotlib.patches as mpatches
from UserSettings import *

#==============================================================
# This program reads in iMET and campus weather station data and makes comparison timeseries plots
# Nov 2016, Sytske Kimball
# v9 29 Aug 2017 reads in new format of iMET sensor data. Including RH sensor temperature.
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
        fin[i]  = open("iMET%s-%s-%s.csv" % (ino[i],date,iMETname[i]))
# Open Mesonet input file
if campus!=99:
    finCampus = open("CampusWest-%s.csv" % (date))
    fin1min = open("CampusWest-1minave-%s.csv" % (date))

#starthour=99
#startmin=99

for i in range(sens+1):
# Read in iMET data.
    if (ino[i]!=99):
        count=0
        index=0
# Skip header line, by reading it.
        dummy=fin[i].readline()
        for row in fin[i]:
            if(iMETformat[i]==0):
                stringlist=row.split(",")    
                for k in range(len(stringlist)):
                    if (len(stringlist[k])==0):
                        stringlist[k]=np.nan    
                timestamp=stringlist[6]
                indate=stringlist[5]
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
                senstemp=999.99
                latin=float(stringlist[7])/10000000.
                lonin=float(stringlist[8])/10000000.
                elevin=(float(stringlist[9])/1000.) - 50.
                satsin=int(stringlist[10])                        
            if(iMETformat[i]==1):
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
            if(iMETformat[i]==2):
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
                if(np.isnan(RHiMETsec[i,index,second]) or np.isnan(tempiMETsec[i,index,second]) or senstemp==999.99):
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
  
print "Plot Stuff"
          
##Plot temperature data
#######################    
figure1 = plt.figure(figsize = (25, 15))
plot1 = figure1.add_subplot(1,1,1)
# Plot temperature
for i in range(sens+1):
    if ino[i]!=99:
        plot1.plot(range(minutes), tempiMET[ino[i]], linewidth=3.0, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
if campus!=99:
    num=11
    plot1.plot(range(minutes), temp150, linewidth=2.0, linestyle='--', color=plotcolmeso[0], label=legendlabelmeso[num])
    num=0
    plot1.plot(range(minutes), temp2m, linewidth=2.0, color=plotcolmeso[0], label=legendlabelmeso[num])   
    num=12
    plot1.plot(range(minutes), temp950, linewidth=2.0, linestyle='--', color=plotcolmeso[1], label=legendlabelmeso[num])
    num=1
    plot1.plot(range(minutes), temp10m, linewidth=2.0, color=plotcolmeso[1], label=legendlabelmeso[num])    

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
plot1.legend(loc=2)
plot1.grid(which='both',axis='both',color='LightGrey',linestyle='dotted')

# Write average values:
if (minutes < 45):
    offset=10
else:
    offset=25
    
plot1.text(minutes-offset,Tmax+4.3*Tinc,"Average Values:",horizontalalignment='left',fontsize=18,fontweight='bold')
plot1.text(minutes-offset,Tmax+3.3*Tinc,"2m T = %5.2f $^{o}$C" % (avetemp2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,Tmax+2.3*Tinc,"10m T = %5.2f $^{o}$C" % (avetemp10m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,Tmax+1.3*Tinc,"2m RH = %5.2f " % (averh2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,Tmax+0.3*Tinc,"10m RH = %5.2f " % (averh10m),horizontalalignment='left',fontsize=18,fontweight='normal')

plot1.text(minutes-5,Tmax+3.3*Tinc,"2m wind = %5.2f m s$^{-1}$" % (avespeed2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,Tmax+2.3*Tinc,"10m wind = %5.2f m s$^{-1}$" % (avespeed10m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,Tmax+1.3*Tinc,"pressure = %7.2f mb" % (avepressure),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,Tmax+0.3*Tinc,"radiation = %5.2f W m$^{-2}$" % (averadiation),horizontalalignment='left',fontsize=18,fontweight='normal')

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
figure1.savefig("iMET-Tower-TempComparison-%s-1minave.png" % (date))
plt.close(figure1)

##Plot RH sensor temperature data
#################################    
figure1 = plt.figure(figsize = (25, 15))
plot1 = figure1.add_subplot(1,1,1)
# Plot temperature
for i in range(sens+1):
    if (ino[i]!=99 and iMETformat[i]!=0):
        plot1.plot(range(minutes), RHtemp[ino[i]], linewidth=3.0, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
if campus!=99:
    num=11
    plot1.plot(range(minutes), temp150, linewidth=2.0, linestyle='--', color=plotcolmeso[0], label=legendlabelmeso[num])
    num=0
    plot1.plot(range(minutes), temp2m, linewidth=2.0, color=plotcolmeso[0], label=legendlabelmeso[num])   
    num=12
    plot1.plot(range(minutes), temp950, linewidth=2.0, linestyle='--', color=plotcolmeso[1], label=legendlabelmeso[num])
    num=1
    plot1.plot(range(minutes), temp10m, linewidth=2.0, color=plotcolmeso[1], label=legendlabelmeso[num])    

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
if (minutes < 45):
    offset=10
else:
    offset=25
    
plot1.text(minutes-offset,TRHmax+4.3*TRHinc,"Average Values:",horizontalalignment='left',fontsize=18,fontweight='bold')
plot1.text(minutes-offset,TRHmax+3.3*TRHinc,"2m T = %5.2f $^{o}$C" % (avetemp2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,TRHmax+2.3*TRHinc,"10m T = %5.2f $^{o}$C" % (avetemp10m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,TRHmax+1.3*TRHinc,"2m RH = %5.2f " % (averh2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-offset,TRHmax+0.3*TRHinc,"10m RH = %5.2f " % (averh10m),horizontalalignment='left',fontsize=18,fontweight='normal')

plot1.text(minutes-5,TRHmax+3.3*TRHinc,"2m wind = %5.2f m s$^{-1}$" % (avespeed2m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,TRHmax+2.3*TRHinc,"10m wind = %5.2f m s$^{-1}$" % (avespeed10m),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,TRHmax+1.3*TRHinc,"pressure = %7.2f mb" % (avepressure),horizontalalignment='left',fontsize=18,fontweight='normal')
plot1.text(minutes-5,TRHmax+0.3*TRHinc,"radiation = %5.2f W m$^{-2}$" % (averadiation),horizontalalignment='left',fontsize=18,fontweight='normal')

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
figure1.savefig("iMET-Tower-RHTempComparison-%s-1minave.png" % (date))
plt.close(figure1)

## Plot RH
###########
figure2 = plt.figure(figsize = (25, 15))
plot1 = figure2.add_subplot(1,1,1)
for i in range(sens+1):
    if ino[i]!=99:
        plot1.plot(range(minutes), RHiMET[ino[i]], linewidth=3.0, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
        plot1.plot(range(minutes), RHadjust[ino[i]], linewidth=3.0, linestyle='--', color=plotcoliMET[ino[i]])
if campus!=99:
    num=2
    plot1.plot(range(minutes), rh2m, linewidth=2.0, color=plotcolmeso[0], label=legendlabelmeso[num])
    num=3
    plot1.plot(range(minutes), rh10m, linewidth=2.0, color=plotcolmeso[1], label=legendlabelmeso[num])

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
figure2.savefig("iMET-Tower-RHComparison-%s-1minave.png" % (date))
plt.close(figure2)

## Plot wind speed and direction
################################
if campus!=99:
    figure3 = plt.figure(figsize = (25, 15))
    plot1 = figure3.add_subplot(1,1,1)

    num=4
    plot1.scatter(range(minutes), dir2m, linewidth=2.0, color=plotcolmeso[0], label=legendlabelmeso[num])
    num=5
    plot1.scatter(range(minutes), dir10m, linewidth=2.0, color=plotcolmeso[1], label=legendlabelmeso[num])

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
    figure3.savefig("iMET-Tower-WindComparison-%s-1minave.png" % (date))
    plt.close(figure3)

### Plot weather station and iMET pressures
###########################################
figure4 = plt.figure(figsize = (25, 15))
plot1 = figure4.add_subplot(1,1,1)
for i in range(sens+1):
    if ino[i]!=99:
        plot1.plot(range(minutes), presiMET[ino[i]], linewidth=3.0, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
if campus!=99:
    num=8
    plot1.plot(range(minutes), pressure1, linewidth=2.0, color=plotcolmeso[0], label=legendlabelmeso[num])
    num=9
    plot1.plot(range(minutes), pressure2, linewidth=2.0, color=plotcolmeso[1], label=legendlabelmeso[num])
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
figure4.savefig("iMET-Tower-PressureComparison-%s-1minave.png" % (date))
plt.close(figure4)

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
plot1.text(1,latmax+2*latinc,"Latitude Comparison %s " % (date),fontsize=22,fontweight='bold')
#plot1.text(-2,latmin-2*latinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')

# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
plot1 = figure5.add_subplot(1,1,1)
figure5.savefig("iMET-Tower-LatitudeComparison-%s-1minave.png" % (date))
plt.close(figure5)
               
### Plot Temperature difference compared to 2m tower sensor
###########################################################
figureTdiff = plt.figure(figsize = (25, 15))
plot1 = figureTdiff.add_subplot(1,1,1)
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=tempiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((temp2m-plotarray)/temp2m)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (temp2m-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num]) 
plot1.plot(range(minutes), minerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[0]) 
plot1.plot(range(minutes), maxerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[0]) 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[0]) 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffmin=-10
Tdiffmax=10
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
plot1.text(1,Tdiffmax+2*Tdiffinc,"Temperature difference with 2m T %s " % (date),fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureTdiff.savefig("2mTempDiffError-%s-1minave.png" % (date))
plt.close(figureTdiff)
        
### Plot Temperature difference compared to 10m tower sensor
############################################################
figureTdiff = plt.figure(figsize = (25, 15))
plot1 = figureTdiff.add_subplot(1,1,1)
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=tempiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((temp10m-plotarray)/temp10m)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (temp10m-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num]) 
plot1.plot(range(minutes), minerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[1]) 
plot1.plot(range(minutes), maxerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[1]) 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[1]) 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffmin=-10
Tdiffmax=10
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
plot1.text(1,Tdiffmax+2*Tdiffinc,"Temperature difference with 10m T %s " % (date),fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureTdiff.savefig("10mTempDiffError-%s-1minave.png" % (date))
plt.close(figureTdiff)

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
plot1.plot(range(minutes), minRHerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[2]) 
plot1.plot(range(minutes), maxRHerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[2]) 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[2])
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
RHdiffmin=-30
RHdiffmax=30
RHdiffinc=2
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
plot1.text(1,RHdiffmax+RHdiffinc,"RH difference with 2m RH %s " % (date),fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureRHdiff.savefig("2mRHDiffError-%s-1minave.png" % (date))
plt.close(figureRHdiff)
        
### Plot RH difference compared to 10m tower sensor
###################################################
figureRHdiff = plt.figure(figsize = (25, 15))
plot1 = figureRHdiff.add_subplot(1,1,1)
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=RHiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((rh10m-plotarray)/rh10m)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num]) 
            plot1.plot(range(minutes), (rh10m-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
plot1.plot(range(minutes), minRHerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[3]) 
plot1.plot(range(minutes), maxRHerror, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[3]) 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black", label=legendlabelmeso[3]) 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
RHdiffmin=-30
RHdiffmax=30
RHdiffinc=2
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
plot1.text(1,RHdiffmax+RHdiffinc,"RH difference with 10m RH %s " % (date),fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureRHdiff.savefig("10mRHDiffError-%s-1minave.png" % (date))
plt.close(figureRHdiff)

##Plot dew point temperature data
#################################    
figure6 = plt.figure(figsize = (25, 15))
plot1 = figure6.add_subplot(1,1,1)
# Plot temperature
for i in range(sens+1):
    if ino[i]!=99:
        plot1.plot(range(minutes), tdewiMET[ino[i]], linewidth=3.0, color=plotcoliMET[ino[i]], label=legendlabeliMET[ino[i]])
if campus!=99:
    num=0
    plot1.plot(range(minutes), tdew2m, linewidth=2.0, color=plotcolmeso[0], label=legendlabelmeso[num])   
    num=1
    plot1.plot(range(minutes), tdew10m, linewidth=2.0, color=plotcolmeso[1], label=legendlabelmeso[num])    

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
figure6.savefig("iMET-Tower-DewPointComparison-%s-1minave.png" % (date))   
plt.close(figure6)

### Plot Temperature difference compared to the averaged iMET temperature
#########################################################################
figureTdiff2 = plt.figure(figsize = (25, 15))
plot1 = figureTdiff2.add_subplot(1,1,1)
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=tempiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((tempave-plotarray)/tempave)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (tempave-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])
plot1.plot(range(minutes), minerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), maxerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black") 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffmin=-1
Tdiffmax=1
Tdiffinc=0.1
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
plot1.text(1,Tdiffmax+1.5*Tdiffinc,"Temperature difference with average iMET T %s " % (date),fontsize=22,fontweight='bold')
plot1.text(1,Tdiffmax+0.5*Tdiffinc,"NOTE: iMET average comparison not meaningful for 10m flights because 2m iMETs included in average.",fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureTdiff2.savefig("iMETaveTempDiffError-%s-1minave.png" % (date)) 
plt.close(figureTdiff2)
 
### Plot RH difference compared to the averaged iMET RH
#######################################################
figureRHdiff = plt.figure(figsize = (25, 15))
plot1 = figureRHdiff.add_subplot(1,1,1)
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=RHiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((RHave-plotarray)/RHave)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (RHave-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num]) 
plot1.plot(range(minutes), minRHerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), maxRHerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black") 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffmin=-15
Tdiffmax=15
Tdiffinc=1
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
plot1.text(1,Tdiffmax+1.5*Tdiffinc,"RH difference with average iMET RH, %s " % (date),fontsize=22,fontweight='bold')
plot1.text(1,Tdiffmax+0.5*Tdiffinc,"NOTE: iMET average comparison not meaningful for 10m flights because 2m iMETs included in average.",fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureRHdiff.savefig("iMETaveRHDiffError-%s-1minave.png" % (date)) 
plt.close(figureRHdiff)  

### Plot pressure difference compared to the averaged iMET pressure
###################################################################
figurepdiff = plt.figure(figsize = (25, 15))
plot1 = figurepdiff.add_subplot(1,1,1)
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=presiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), ((presave-plotarray)/presave)*100, linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (presave-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
plot1.plot(range(minutes), minperror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), maxperror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black") 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffmin=-1
Tdiffmax=1
Tdiffinc=0.1
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
plot1.text(1,Tdiffmax+1.5*Tdiffinc,"Pressure difference with average iMET pressure, %s " % (date),fontsize=22,fontweight='bold')
plot1.text(1,Tdiffmax+0.5*Tdiffinc,"NOTE: iMET average comparison not meaningful for 10m flights because 2m iMETs included in average.",fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figurepdiff.savefig("iMETavePresDiffError-%s-1minave.png" % (date))   
plt.close(figurepdiff)

### Plot Dew Point Temperature differences compared to the averaged iMET dew point temperature
##############################################################################################
figureTdiff3 = plt.figure(figsize = (25, 15))
plot1 = figureTdiff3.add_subplot(1,1,1)
for i in range(sens+1):
    if(ino[i]!=99):
        plotarray=tdewiMET[i]
        if(campus!=99):
            num=ino[i]
#            plot1.plot(range(minutes), (tdewave-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
            plot1.plot(range(minutes), (tdewave-plotarray), linewidth=1.2, color=plotcoliMET[num], label=legendlabeliMET[num])  
plot1.plot(range(minutes), mindewerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), maxdewerror, linewidth=1.2, linestyle="--", color="black") 
plot1.plot(range(minutes), zeroline, linewidth=1.2, linestyle="--", color="black") 
plot1.set_xlim([0,minutes])
plot1.set_xticks(np.linspace(0,minutes,(minutes/delx)+1))
plot1.set_xticklabels(timelabel, rotation=90, ha='center', fontsize = 12)
Tdiffmin=-5
Tdiffmax=5
Tdiffinc=0.5
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
plot1.text(1,Tdiffmax+1.5*Tdiffinc,"Dew Point Temperature difference with average iMET Tdew %s " % (date),fontsize=22,fontweight='bold')
plot1.text(1,Tdiffmax+0.5*Tdiffinc,"NOTE: iMET average comparison not meaningful for 10m flights because 2m iMETs included in average.",fontsize=22,fontweight='bold')
#    plot1.text(-2,Tdiffmin-2*Tdiffinc,"%s:%s CST " % (starthour,startmin),fontsize=16,fontweight='normal')
# put legend in upper left corner
plot1.legend(loc=2)
# Write the plot to a file 
figureTdiff3.savefig("iMETaveTdewDiffError-%s-1minave.png" % (date)) 
plt.close(figureTdiff3)

# Write out Temperature values to check
#print "Time   Mesonet     iMET3     iMET5     iMET7     iMET9     iMET10    iMET11    iMET12    iMET13    iMET15    iMET16     iMET17    iMET18    iMET19    iMET20    iMET21    iMET22"
##for i in range(minutes):
#    print timelabel[i].rjust(3),"%9.2f" %(temp2m[i]),"%9.2f" %(tempiMET[3,i]),"%9.2f" %(tempiMET[5,i]),"%9.2f" %(tempiMET[7,i]),"%9.2f" %(tempiMET[9,i]),"%9.2f" %(tempiMET[10,i]),"%9.2f" %(tempiMET[11,i]),"%9.2f" %(tempiMET[12,i]),"%9.2f" %(tempiMET[13,i]),"%9.2f" %(tempiMET[15,i]),"%9.2f" %(tempiMET[16,i]),"%9.2f" %(tempiMET[17,i]),"%9.2f" %(tempiMET[18,i]),"%9.2f" %(tempiMET[19,i]),"%9.2f" %(tempiMET[20,i]),"%9.2f" %(tempiMET[21,i]),"%9.2f" %(tempiMET[22,i])

print "VAR       iMET3    iMET4    iMET5    iMET6    iMET7    iMET8    iMET9   iMET10   iMET11   iMET12   iMET13   iMET14   iMET15   iMET16   iMET17   iMET18"
#for i in range(minutes):
i=10
print ("Temp  ".rjust(0)),
for j in range(3,19):
    print ("%8.2f" %(tempiMET[j,i])),
print(' ')
print ("Tdew  ".rjust(0)),
for j in range(3,19):
    print ("%8.2f" %(tdewiMET[j,i])),
print(' ')
print ("Pres  ".rjust(0)),
for j in range(3,19):
    print ("%8.2f" %(presiMET[j,i])),
print(' ')
print ("RH    ".rjust(0)),
for j in range(3,19):
    print ("%8.2f" %(RHiMET[j,i])),
print(' ')
print ("RHTemp".rjust(0)),
for j in range(3,19):
    print ("%8.2f" %(RHtemp[j,i])),
print(' ')

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
    fout2m=open("%s.dat" % (name),"w")  
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
    fout10m=open("%s.dat" % (name),"w")  
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
    fout2m=open("%s.dat" % (name),"w")  
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
    fout2m=open("%s.dat" % (name),"w")  
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