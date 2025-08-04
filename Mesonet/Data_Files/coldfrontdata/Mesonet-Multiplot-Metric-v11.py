import csv
import numpy as np
import matplotlib.pyplot as plt
import math
#from pylab import *
import matplotlib.patches as mpatches

#==============================================================
# Code by S. Kimball
# 20 Nov 2021 --- version 11:
# Added in a separate axis for equivalent potential temperature.
# Lined up all axis labels and legends.
# version 10 includes an option to plot the surface temperature.
# This program reads campus weather station data and makes multi-plot timeseries plots Mar 2017, Sytske Kimball
# Download from Mesonet page using the Select All Option - so you don't have to select individual parameters - Jan 2019
# You can now download and plot more than 2 day. Set the number of days under variable "days" below. Aug 2019
# Data will automatically come down for full 24 hour days (i.e. 00:00 through 23:59); you cannot select a start or end hour.
# This program *will* give you an option to plot only part of the downloaded data; set startday, hour, minute and enday, hour and minute below - Aug 2019
# Version 6 (18 Sep 2020) includes:
#   wind gust
#   option to plot in metric or English
#   option to put CDT on x axis label
# Version 9 (21 May 2021) includes:
#   fixed the way the indices were calculated (now using day-1 instead of day)
#   allows multiple months in a year to be plotted 
#   date labels now include the start and end month as does the file name
#   all months have to be within the same year and they have to be sequential
#   if the year is a leapyear, that is automatically accounted for
#==============================================================

#==============================================================
# User Settings... 
#==============================================================
#StationFullName=['Agricola','Atmore','Andalusia','Ashford North','Castleberry','Dixie','Dog River','Elberta','Fairhope','Foley','Florala','Gasque','Geneva','Grand Bay','Jay','Kinston','Leakesville','Loxley','Mount Vernon','Pascagoula','Poarch Creek','Robertsdale','Saraland','USA Campus']
#Stationlist=['Agr','Atm','And','AshN','Cast','Dix','DogR','Elb','Fair','Fol','Flo','Gas','Gen','Gran','Jay','Kin','Leak','Lox','MtV','Pas','Poarch','Rob','Sar','USAW']
#StationID  =[201,  501,  702  ,1001,   1301,  502,  305,   403,  404,   405,  701,  407,  901,  304,   1601, 1401, 1201,  406,  301,  101,  503,     402,  306,  307]

StationFullName=['USA Campus West']
Stationlist=['USAW']
StationID = [307]

date='22Nov2021'
#### !!!!!! Also set ranges of dates to plot !!!!!!!!
startmonth=11
startday=22
starthour=0
startmin=0
endmonth=11
endday=22
endhour=23
endmin=59
# Set time (x) axis label increment in minutes
delx=60

# Add one because arrays start with index 0
leapyears=[2004,2008,2012,2016,2020,2024,2028,2032]
year=int(date[-4:])
if (year in leapyears):
    monthdays=[99,31,60,91,121,152,182,213,244,274,305,335,366]
else:
    monthdays=[99,31,59,90,120,151,181,212,243,273,304,334,365]
startindex=monthdays[startmonth-1]*24*60+(startday-1)*24*60+starthour*60+startmin
endindex=monthdays[endmonth-1]*24*60+(endday-1)*24*60+(endhour)*60+endmin
minutes=endindex-startindex+1
datelabel=["" for i in range(minutes)]

casename='Cold Front'

#Fontsizes
# for legend labels
legendsize=24
# For y axis labels
labelsize=28
# For x axis labels
xlabelsize=24
# For everything else
lettersize=36

# Slect which varianles to plot - set yes or no (no caps).
Dewpoint='yes'
EquivalentPotTemp='no'
# 10 m wind
WindDirection='yes'
WindGust='no'
# 2 m wind speed
WindSpeed2m='no'
# 10 m wind speed
WindSpeed10m='yes'
Temperature150cm='yes'
Temperature200cm='yes'
Temperature950cm='no'
Temperature1000cm='yes'
SurfaceTemp='no'
pressure='yes'
radiationplot='yes'
RainfallRate='no'
RainfallTotal='no'
#Vertical wind speed
vertical='no'
# Plot in metric or English. If 'no' winds will be in mph, temperatures in F, rainfall in inches.
metric='yes'
# If want CDT on x axis label set CDT=yes. But be careful it does not incorporate going into a new month or year. Only the hour and day are adjusted.
CDT='no'

# Set radiation limits and axis increment
radmin=0.0
radmax=1200.0
radinc=50.0
# Set pressure limits
presmin= 1006.0
presmax=1020.0
presinc=1.0
# Set temperature axis range and increment for plotting; if metric='no', use English units
Tmin=0.0
Tmax=20.0
Tinc=2.0
# Thetae axis range limits
Themin=330
Themax=360
Theinc=2.0
# Set wind speed max values (min=0); if metric='no', use English units
windmax=10
windinc=1
# Set windspeed value where w=0 will be plotted.
vertoffset=10
# Set rainfall limits; if metric='no', use English units
rainmin=0.
rainmax=10.0
raininc=1.0
# Specific heat of dry air
cp=1004.0
# Gas constant of dry air
Rd=287.04
# Reference pressure in mb
p0=1000.0
# Laten heat of vaporization
Lv = 2.501E6

# Assume only 3 hours of data are collected (this is an ok assumption because the iMET battery lasts only 80 minutes).
# Plotcolors
#plotcoliMET = [" ","Tan","Maroon","turquoise","darkmagenta","fuchsia","teal","lightgreen","Gold","MediumVioletRed","Coral"]
#plotcolmeso = ["royalblue","navy","royalblue","navy","royalblue","navy","royalblue","navy","royalblue","navy","navy","royalblue","navy"]
#legendlabelmeso = ["2m T ","10m T ","2 m RH","10 m RH","2 m wind dir","10 m wind dir","2 m wind speed","10 m wind speed","pressure1","pressure2","latitude","1.5m T","9.5m T"]
months = ["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

#Open Statistics Output file
fout = open("Statistics-%s-%s.txt" % (casename,date), "w" )
    
for Station in Stationlist:
    xlabel=["" for i in range(int(minutes/delx)+1)]
    ## Weather Station Data
    #Initialize the full array with NaN to account for missing data
    Tsfc      = np.full((minutes),np.nan,dtype=float)
    temp2m    = np.full((minutes),np.nan,dtype=float)
    temp150   = np.full((minutes),np.nan,dtype=float)
    temp10m    = np.full((minutes),np.nan,dtype=float)
    temp950   = np.full((minutes),np.nan,dtype=float)
    speed10m  = np.full((minutes),np.nan,dtype=float)
    gust10m   = np.full((minutes),np.nan,dtype=float)
    dir10m    = np.full((minutes),np.nan,dtype=float)
    speed2m   = np.full((minutes),np.nan,dtype=float)
    rh2m      = np.full((minutes),np.nan,dtype=float)
    tdew2m    = np.full((minutes),np.nan,dtype=float)
    radiation = np.full((minutes),np.nan,dtype=float)
    pressure1 = np.full((minutes),np.nan,dtype=float)
    pressure2 = np.full((minutes),np.nan,dtype=float)
    precipTB3 = np.full((minutes),np.nan,dtype=float)
    precipTE  = np.full((minutes),np.nan,dtype=float)
    raintotTB3 = np.full((minutes),np.nan,dtype=float)
    raintotTE  = np.full((minutes),np.nan,dtype=float)
    thetae    = np.full((minutes),np.nan,dtype=float)
    vertwind  = np.full((minutes),np.nan,dtype=float)
    
    # Open Mesonet input file
    finMeso = open("%s-%s.csv" % (Station,date))
        
    # read the header line
    dummy=finMeso.readline()
    countcamp=0
    index=0
    raintotTB3[0]=0.0
    raintotTE[0]=0.0
    for row in finMeso:
    # For comma deliminated input:
        stringlist=row.split(",")    
        for k in range(len(stringlist)):
            if (len(stringlist[k])==0):
                stringlist[k]='nan'
    # Check date
        timestamp=stringlist[0]
        indate=timestamp.split(' ')[0]
        month=int(indate.split('/')[0])
        day=int(indate.split('/')[1])
        year=indate.split('/')[2]
        intime=timestamp.split(' ')[1]
        hour=int(intime.split(':')[0])
        minute=int(intime.split(':')[1])
        idate=str(day)+months[month]+year
        if(countcamp==0):
            # Check that the file is for the correct station
            if(Stationlist[StationID.index(int(stringlist[9]))]!=Station):
                print ("File is not for station", Station)
            if(startmonth==endmonth):
                date4plot=str(startday)+' - '+str(endday)+' '+months[startmonth]+' '+year
            else:
                date4plot=str(startday)+' '+months[startmonth]+' - '+str(endday)+' '+months[endmonth]+' '+year
            #if(idate!=date):
            #    print "WARNING: wrong date (",idate,") for Mesonet Station"
        dataindex=monthdays[month-1]*24*60+(day-1)*24*60 + hour*60 + minute
        if(startindex<=dataindex and dataindex<=endindex):  
            index=dataindex-startindex          
    # Fill the date label array ********** NEED TO ADD THE DAY AND MONTH*********************
            if(CDT=='yes'):
               hourlabel=hour+1
               daylabel=day
               if(hour==23): 
                   hourlabel=0
                   daylabel=day+1
            else:
                hourlabel=hour
                daylabel=day
            if(minute<10):
                datelabel[index]=str(hourlabel)+':'+'0'+str(minute)+' '+str(daylabel)+' '+months[month]+' '+str(year)
            else:
                datelabel[index]=str(hourlabel)+':'+str(minute)+' '+str(daylabel)+' '+months[month]+' '+str(year)
            if(metric=='no'):
                precipTB3[index]=float(stringlist[17])/25.4
                precipTE[index]=float(stringlist[18])/25.4
            else:
                precipTB3[index]=float(stringlist[17])
                precipTE[index]=float(stringlist[18])
            if(index > 0):
                raintotTB3[index]=raintotTB3[index-1]+precipTB3[index]
                raintotTE[index]=raintotTE[index-1]+precipTE[index]
            if(metric=='no'):
                temp2m[index]=float(stringlist[31])*9./5. + 32.
                temp150[index]=float(stringlist[30])*9./5. + 32.
                temp10m[index]=float(stringlist[33])*9./5. + 32.
                temp950[index]=float(stringlist[32])*9./5. + 32. 
                Tsfc[index]=float(stringlist[24])*9./5. + 32. 
            else:
                temp2m[index]=float(stringlist[31])
                temp150[index]=float(stringlist[30])  
                temp10m[index]=float(stringlist[33])
                temp950[index]=float(stringlist[32])   
                Tsfc[index]=float(stringlist[24])
            rh2m[index]=float(stringlist[34])
            pressure1[index]=float(stringlist[36])  
            pressure2[index]=float(stringlist[37])
            # column 38 is TR and column 39 is QR
            radiation[index]=float(stringlist[39])
            if(metric=='no'):
                # Maximum 10m windspeed
                gust10m[index]=float(stringlist[50])*3600./1609.
                # Scalar mean wind speed at 10m
                speed10m[index]=float(stringlist[70])*3600./1609.
                # Vertical wind speed at 10 m
                vertwind[index]=float(stringlist[44])*3600./1609.
                # scalar mean wind speed at 2m
                speed2m[index]=float(stringlist[66])*3600./1609.
            else:
                # Maximum 10m windspeed
                gust10m[index]=float(stringlist[50])
                # Scalar mean wind speed at 10m
                speed10m[index]=float(stringlist[70])
                # Vertical wind speed at 10 m
                vertwind[index]=float(stringlist[44])
                # scalar mean wind speed at 2m
                speed2m[index]=float(stringlist[66])
            dir10m[index]=float(stringlist[72])
    # Calculate Tdew. e and esat are in mb; temp2in is in C; Tdew is in C
            esat=6.1365*math.exp((17.502*temp2m[index])/(240.97+temp2m[index]))
            e=rh2m[index]*esat/100.0
            if(e <=0.0):
                tdew2m[index]='nan'           
            else:
                tdew2m[index]=240.97*math.log(e/6.1365)/(17.502-math.log(e/6.1365))  
    # Calculate thetae - formula from Atmospheric Thermodynamics by Bohren and Albrecht, formula 6.126, pg 294.
    # TLCL is calculated from their formula 6.35 on pg 278.
    # theta and thetae are in K.
            if(EquivalentPotTemp=='yes'):
                theta=(temp2m[index]+273.15)*(pressure1[index]/p0)**(-Rd/cp)
                TLCL = (9.8*tdew2m[index] - 1.8*temp2m[index])/8.0
                TLCL = TLCL + 273.15
                w = 0.622*e/(pressure1[index]-e)
                thetae[index]=theta*math.exp(Lv*w/(cp*TLCL))
        countcamp = countcamp + 1      
    finMeso.close()
    
    print ("Plot Stuff for ", Station)
            
    ##Plot data
    #######################    
    figure1, plot1 = plt.subplots(figsize = (50, 16))
    # Twin the x-axis twice to make independent y-axes.
    plot2=plot1.twinx()
    if(pressure=='yes'):
        plot3=plot1.twinx()
    if(RainfallRate=='yes' or RainfallTotal=='yes'):
        plot4=plot1.twinx()
    if(EquivalentPotTemp=='yes'):
        plot5=plot1.twinx()
    
    # Make some space on the right side for the extra y-axis.
    #figure1.subplots_adjust(left=0.75)
    # Move the last y-axis spine over to the right by 20% of the width of the axes
    #plot3.spines['right'].set_position(('axes', 1.2))
    
    # Make some space on the left side for the extra y-axis.
    figure1.subplots_adjust(left=0.20)
    # Make some space on the bottom for larger x-axis labels
    figure1.subplots_adjust(bottom=0.20)
    figure1.subplots_adjust(top=0.88)
    # Move the last y-axis right spine over to the left by 10% of the width of the axes
    if(pressure=='yes'):
        plot3.spines['right'].set_position(('axes', -0.13))
    if(RainfallRate=='yes' or RainfallTotal=='yes'):
        plot4.spines['right'].set_position(('axes', -0.06))
    if(EquivalentPotTemp=='yes'):
        plot5.spines['right'].set_position(('axes', -0.21))

    # To make the border of the right-most axis visible, we need to turn the frame
    # on. This hides the other plots, however, so we need to turn its fill off.
    if(pressure=='yes'):
        plot3.set_frame_on(True)
        plot3.patch.set_visible(False)
    if(RainfallRate=='yes' or RainfallTotal=='yes'):
        plot4.set_frame_on(True)
        plot4.patch.set_visible(False)
    if(EquivalentPotTemp=='yes'):
        plot5.set_frame_on(True)
        plot5.patch.set_visible(False)
    
    # And finally we get to plot things...
    if(Temperature1000cm=='yes'):
        plot1.plot(range(minutes), temp10m, linewidth=3, color='DarkBlue', label='10m Temperature')      
    if(Temperature950cm=='yes'):    
        plot1.plot(range(minutes), temp950, linewidth=3, linestyle=':', color='RoyalBlue', label='9.5m Temperature')
    if(Temperature200cm=='yes'):
        plot1.plot(range(minutes), temp2m, linewidth=3, color='DodgerBlue', label='2m Temperature')  
    if(Temperature150cm=='yes'):    
        plot1.plot(range(minutes), temp150, linewidth=3, linestyle=':', color='LightSkyBlue', label='1.5m Temperature')
    if (Dewpoint=='yes'):
        plot1.plot(range(minutes), tdew2m, linewidth=3, linestyle='-', color= 'Purple', label='2m Dewpoint Temperature')
    if (SurfaceTemp=='yes'):
        plot1.plot(range(minutes), Tsfc, linewidth=3, linestyle='-', color= 'Brown', label='Surface Temperature')
    
    plot1.set_xlim([0,minutes])
    plot1.set_xticks(np.linspace(0,minutes,int(minutes/delx)+1))
    for i in range(int(minutes/delx)):
        xlabel[i]=datelabel[i*delx]
    # apply offset to all x-axis labels
    #for label in plot1.xaxis.get_majorticklabels():
    #    label.set_transform(label.get_transform() + 0.2)
    # The rotation_mode argument lets the rotation happen about the top left point of the text instead of the center.
    plot1.set_xticklabels(xlabel, rotation=45, ha='right', rotation_mode="anchor",fontsize = xlabelsize)
    plot1.set_ylim([Tmin,Tmax])
    plot1.set_yticks(np.arange(Tmin,Tmax+0.1,Tinc))
    # Make the y labels bigger.
    for label in plot1.get_yticklabels():
        label.set_size(labelsize)
        label.set_color('royalblue')
    if(CDT=='no'):
        plot1.set_xlabel("Time (CST)",fontsize = lettersize)
    else:
        plot1.set_xlabel("Time (CDT)",fontsize = lettersize)
    plot1.text(-0.20,1.04,"%s %s " % (StationFullName[Stationlist.index(Station)],date4plot),transform=plot1.transAxes,fontsize=lettersize)
    plot1.grid(which='both',axis='both',color='LightGrey',linestyle='dotted')
    
    # Plot 10m wind direction
    if(WindDirection=='yes'):
        plot2.scatter(range(minutes), (dir10m*windmax/360), linewidth=0.05, color='SlateBlue', label='Wind Direction')
    # Plot scaled radiation
    if(radiationplot=='yes'):
        a=windmax/(radmax-radmin)
        b=-a*radmin
    ##a=36/(radmax-radmin)
    ##b=-a*radmin
        plot2.plot(range(minutes), (radiation*a + b), linewidth=2.0, linestyle='-', color='sandybrown', label="Scaled Total Radiation")
    # Plot wind speed
    if(WindSpeed10m=='yes'):
        plot2.plot(range(minutes), speed10m, linewidth=1.0, linestyle='-', color='MediumSeaGreen', label="10m Wind Speed")
    if(WindGust=='yes'):
        plot2.plot(range(minutes), gust10m, linewidth=2.0, linestyle='-', color='Aquamarine', label="Wind Gust")
    if(vertical=='yes'):
        plot2.plot(range(minutes), (vertwind+vertoffset), linewidth=2, linestyle='-', color='coral',  label="Vertical wind speed")
    if(WindSpeed2m=='yes'):
        plot2.plot(range(minutes), speed2m, linewidth=1.0, linestyle='-', color='Teal', label="2m Wind Speed")
    # Plot scaled pressure
    #a=36/(presmax-presmin)
    #b=-a*presmin
    #if(Pressure=='yes'):
    #    plot2.plot(range(minutes), (a*pressure1 + b), linewidth=2.0, linestyle='-', color='crimson', label='Scaled pressure 1')
    #    plot2.plot(range(minutes), (a*pressure2 + b), linewidth=2.0, linestyle='-', color='orangered', label='Scaled pressure 2')
    # Set y axis range, tick marks etc.
    plot2.set_ylim(0,windmax)
    yticks=[]
    yticks=np.arange(0,windmax+0.1,windinc)
    plot2.get_yaxis().get_major_formatter().set_useOffset(False)
    plot2.set_yticks(yticks)
    for label in plot2.get_yticklabels():
        label.set_color('Teal')
        label.set_size(labelsize)
    #plot2.set_ylabel(r"Wind Speed (m s$^{-1}$)",fontsize = 26, color='Teal')
    
    # alpha makes the line transparent; the lower the value, the more transparent.
    if(EquivalentPotTemp=='yes'):
        plot5.plot(range(minutes), thetae, linewidth=3, linestyle='-', color= 'Orchid', alpha=0.7, label=r'$\theta_{e}$')
        for label in plot5.get_yticklabels():
            label.set_size(labelsize)
    # 'pad' is the padding space between the tick marks and the number, 'direction' determines which way the tick marks point, 'size' sets the length of the tick marks
        plot5.tick_params(axis='y', colors='Orchid', direction ='in', pad=-60, size = 8)
        plot5.set_ylim([Themin,Themax])
        plot5.set_yticks(np.arange(Themin,Themax+0.1,Theinc))

    # alpha makes the line transparent; the lower the value, the more transparent.
    if(pressure=='yes'):
        plot3.plot(range(minutes), pressure1, linewidth=3, linestyle='-', color= 'crimson', alpha=0.7, label='pressure 1')
        #plot3.plot(range(minutes), pressure2, linewidth=2, linestyle='-', color= 'orangered', alpha=0.7, label='pressure 2')
        for label in plot3.get_yticklabels():
            label.set_size(labelsize)
        # 'pad' is the padding space between the tick marks and the number, 'direction' determines which way the tick marks point, 'size' sets the length of the tick marks
        plot3.tick_params(axis='y', colors='crimson', direction ='in', pad=-85, size = 8)
        plot3.set_ylim([presmin,presmax])
        plot3.set_yticks(np.arange(presmin,presmax+0.1,presinc))
    
    # Plot precip
    if(RainfallRate=='yes'):
        # alpha makes the line transparent; a smaller value is more transparent
        plot4.bar(range(minutes), (precipTB3), linewidth=2, align='center', color='DarkTurquoise', edgecolor='DarkTurquoise', alpha=0.5, label='TB3 Rainfall rate')
        plot4.bar(range(minutes), (precipTE), linewidth=2, align='center', color='fuchsia', edgecolor='fuchsia', alpha=0.4, label='TE Rainfall rate')  
        for label in plot4.get_yticklabels():
            label.set_size(labelsize)
    # 'pad' is the padding space between the tick marks and the number, 'direction' determines which way the tick marks point, 'size' sets the length of the tick marks
        plot4.tick_params(axis='y', colors='DarkTurquoise', direction ='in', pad=-60, size = 8)
        plot4.set_ylim([rainmin,rainmax])
        plot4.set_yticks(np.arange(rainmin,rainmax+0.1,raininc))
        plot4.legend(loc=2, fontsize=legendsize, framealpha=1.0, bbox_to_anchor=(0.15, 1.18))
    if(RainfallTotal=='yes'):
        # alpha makes the line transparent; a smaller value is more transparent
        plot4.plot(range(minutes), raintotTB3, linewidth=3, linestyle='-', color= 'DarkTurquoise', alpha=0.7, label='TB3 Rainfall total')
        plot4.plot(range(minutes), raintotTE, linewidth=3, linestyle='-', color= 'fuchsia', alpha=0.7, label='TE Rainfall total')
        for label in plot4.get_yticklabels():
            label.set_size(labelsize)
    # 'pad' is the padding space between the tick marks and the number, 'direction' determines which way the tick marks point, 'size' sets the length of the tick marks
        plot4.tick_params(axis='y', colors='DarkTurquoise', direction ='in', pad=-60, size = 8)
        plot4.set_ylim([rainmin,rainmax])
        plot4.set_yticks(np.arange(rainmin,rainmax+0.1,raininc))
        plot4.legend(loc=2, fontsize=legendsize, framealpha=1.0, ncol=2, bbox_to_anchor=(0.16, 1.18))
        
    # Plot legends
    # 'framealpha' is used to make the legend box transparent, the smaller the number, the more transparent.
    # 'ncol' controls the numner of columns the legend has.
    # 'bbox_to_anchor' allows you to move the legend outside the plot area.
    plot2.legend(loc=1, fontsize=legendsize, framealpha=1.0, ncol=2, bbox_to_anchor=(1.06, 1.18))
    plot1.legend(loc=1, fontsize=legendsize, framealpha=1.0, ncol=2, bbox_to_anchor=(0.75, 1.18))
    #plot3.legend(loc=2, fontsize=legendsize, framealpha=1.0, bbox_to_anchor=(-0.05, 1.18))
    
    if(EquivalentPotTemp=='yes' or pressure=='yes'):
        plot3.legend(loc=2, fontsize=legendsize, framealpha=1.0, bbox_to_anchor=(0.02, 1.18))
    #legend2.get_frame().set_facecolor('white')
    #legend1.get_frame().set_facecolor('white')
    
    # Write Wind direction labels
    if(WindDirection=='yes'):
        cardinal=["N","NE","E","SE","S","SW","W","NW","N"]
        offset=1.0/(len(cardinal)-1)
        for i in range(len(cardinal)):
            plot1.text(1.08,-0.013+i*offset,"%s" %(cardinal[i]),transform=plot1.transAxes,fontsize=labelsize,ha='center',fontweight='bold',color='SlateBlue')
    
    # Inner left y-axis label.
    # transform=plot1.transAxes makes the x and y coordinates run from 0 to 1 with (0,0) being the lower left and (1,1) the upper left corner of the plot panel.
    if(metric=='no'):
        plot1.text(-0.04,0.63,"Temperature ($^{o}$F)",transform=plot1.transAxes,fontsize = lettersize, rotation=90, color ='royalblue')
    else:
        plot1.text(-0.04,0.63,"Temperature ($^{o}$C)",transform=plot1.transAxes,fontsize = lettersize, rotation=90, color ='royalblue')
    if (Dewpoint=='yes'):
        if(metric=='no'):
            plot1.text(-0.04,-0.02,"Dew Point Temperature ($^{o}$F)",transform=plot1.transAxes,fontsize = lettersize, rotation=90, color ='purple')
        else:
            plot1.text(-0.04,-0.02,"Dew Point Temperature ($^{o}$C)",transform=plot1.transAxes,fontsize = lettersize, rotation=90, color ='purple')
    # Outer left y-axis label
    if(EquivalentPotTemp=='yes'):
        plot2.text(-0.26,0.10,"Equivalent potential temparature (K)",transform=plot1.transAxes,fontsize=lettersize,color='Orchid',rotation=90)
    # Right y axis label
    if(metric=='no'):
        plot2.text(1.03,0.5,"Wind speed (mph)",transform=plot1.transAxes,fontsize=lettersize,rotation=90,color='Teal')
    else:
        plot2.text(1.03,0.5,"Wind speed (m s$^{-1}$)",transform=plot1.transAxes,fontsize=lettersize,rotation=90,color='Teal')
    if(RainfallRate=='yes' or RainfallTotal=='yes'):
        if (metric=='no'):
            plot2.text(-0.11,0.5,"Rainfall (inch)",transform=plot1.transAxes,fontsize=lettersize,rotation=90,color='DarkTurquoise')
        else:
            plot2.text(-0.11,0.5,"Rainfall (mm)",transform=plot1.transAxes,fontsize=lettersize,rotation=90,color='DarkTurquoise')
    if(pressure=='yes'):
        plot2.text(-0.19,0.5,"Pressure (mb)",transform=plot1.transAxes,fontsize=lettersize,color='crimson',rotation=90)
    
    
    ## Write the plot to a file 
    figure1.savefig("Multiplot-%s-%s.png" % (Station,date4plot))
    plt.close(figure1)
    
    # Write statistics to output file
    fout.write("%s %s statistics for %s\n" %(casename,date,StationFullName[Stationlist.index(Station)]))
    if(metric=='no'):       
        raintot=np.nanmax(raintotTB3)
        fout.write("TB3 rainfall total:                      %8.2f  inches" %raintot)
        fout.write(" \n")
        raintot=np.nanmax(raintotTE)
        fout.write("TE rainfall total:                       %8.2f  inches" %raintot)
        fout.write(" \n")
        windstat=np.nanmax(speed10m)
        fout.write("10 m maximum 1-min sustained wind speed: %8.2f  mph" %windstat)
        fout.write("%8.2f  m/s" %(windstat*1609./3600.))
        fout.write(" \n")
        windstat=np.nanmax(gust10m)
        fout.write("10 m maximum wind gust:                  %8.2f  mph" %windstat)
        fout.write("%8.2f  m/s" %(windstat*1609./3600.))
        fout.write(" \n")
    else:
        raintot=np.nanmax(raintotTB3)
        fout.write("TB3 rainfall total:                      %8.2f  mm" %raintot)
        fout.write(" \n")
        raintot=np.nanmax(raintotTE)
        fout.write("TE rainfall total:                       %8.2f  mm" %raintot)
        fout.write(" \n")
        windstat=np.nanmax(speed10m)
        fout.write("10 m maximum 1-min sustained wind speed: %8.2f  m/s" %windstat)
        fout.write(" \n")
        windstat=np.nanmax(gust10m)
        fout.write("10 m maximum wind gust:                  %8.2f  m/s" %windstat)
        fout.write(" \n")        
    fout.write(" \n")
    fout.write(" \n")
    
fout.close()