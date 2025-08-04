#!/usr/bin/python

from ploteverything import *
import os

print "Every Module Loaded Successfully"

###############Quad Files################

#1-4 for October 25 #1-4 corresponds to 53-56 for pitot sensor

quadFiles = [
    "", #8/24 - No quad used today
    "", #8/30
    "", #9/6
    "", #9/13
    "", #9/20
    "", #9/27
    "", #10/4
    "", #10/11
    "", #10/18
    "", #10/21
    "Quad/Data_Files/10_25_2016/FlightALL.log", #10/25
    "", #11/1
    "", #11/8
    "", #11/15
    "", #11/22
    "Quad/Data_Files/11_29_2016/Flight2.log",  #11/29
    "", #12/6
    "", #12/8
    "", #12/9
    "", #12/15
    "Quad/Data_Files/1_13_2017/Two_Soundings.log", #1/13/2017
    "", #2/7
    ["Compiled_Data/Mesonet_Results/4_13_2017/FASTALLFILES.log","Compiled_Data/Mesonet_Results/4_13_2017/SytskeALLFILES.log"], #4/13/2017
]

################iMet FileName###############


iMetFiles = [
    "iMet/Field_Tests/8_24_2016/truncated_file.csv",   #8/24 - We just went for a walk on this day
    "", #8/30
    "iMet/Field_Tests/9_6_2016/20160906-104920-00043444.csv", #9/6
    "", #9/13
    "",  #9/20
    "", #9/27
    "", #10/4
    "", #10/11
    "", #10/18
    "", #10/21
    "iMet/Field_Tests/10_25_2016/iMET3-25Oct2016-IrisFront.csv", #10/25
    "", #11/1
    "", #11/8
    "", #11/15
    "", #11/22
    "", #11/29
    "", #12/6
    "", #12/8
    ["iMet/Irvington_Flight_Tests/12_9_2016/Iris_Front_2Soundings","iMet/Irvington_Flight_Tests/12_9_2016/Iris_Rear_2Soundings"], #12/9 - Irvington Flight Test - There were two imets on this guy. Not sure how to handle that.
    "", #12/15
    "", #1/13/2017
    "", #2/7
    "", #4/13
]


################Pitot File Name#############
pitotFiles = [
    "", #8/24 - This was an iMet only day
    "FASTPitot/Data_Files/Mesonet_Data_Files/8_30_2016/GPSLOG_ALL.TXT", #8/30
    "FASTPitot/Data_Files/Mesonet_Data_Files/9_6_2016/GPSLOG_ALL.TXT", #9/6
    "FASTPitot/Data_Files/Mesonet_Data_Files/9_13_2016/GPSLOG_ALL.TXT", #9/13
    "FASTPitot/Data_Files/Mesonet_Data_Files/9_20_2016/GPSLOG_ALL.TXT", #9/20
    "FASTPitot/Data_Files/Mesonet_Data_Files/9_27_2016/GPSLOG_ALL.TXT", #9/27
    "FASTPitot/Data_Files/Mesonet_Data_Files/10_4_2016/GPSLOG_ALL.TXT", #10/4
    "FASTPitot/Data_Files/Mesonet_Data_Files/10_11_2016/GPSLOG_ALL.TXT", #10/11
    "FASTPitot/Data_Files/Mesonet_Data_Files/10_18_2016/GPSLOG_ALL.TXT", #10/18
    "FASTPitot/Data_Files/Mesonet_Data_Files/10_21_2016/GPSLOG_ALL.TXT", #10/21
    "FASTPitot/Data_Files/Mesonet_Data_Files/10_25_2016/GPSLOG_ALL.TXT", #10/25 - This is the first day we had 4 flights - This is also the day that I had to pee midflight and had to land
    "FASTPitot/Data_Files/Mesonet_Data_Files/11_1_2016/GPSLOG_ALL.TXT", #11/1 - 4 flights normal
    "FASTPitot/Data_Files/Mesonet_Data_Files/11_8_2016/GPSLOG_ALL.TXT", #11/8 - Rainy day only 3 flights
    "FASTPitot/Data_Files/Mesonet_Data_Files/11_15_2016/GPSLOG_ALL.TXT", #11/15 - 4 flights normal
    "", #11/22 - Whoops day. Flashed incorrect code on pitot
    "FASTPitot/Data_Files/Mesonet_Data_Files/11_29_2016/GPSLOG_ALL.TXT", #11/29 - First day I stopped turning the pitot probe off between flight. Also the first day we crashed the quad on flight #2.
    "FASTPitot/Data_Files/Mesonet_Data_Files/12_6_2016/GPSLOG07.TXT", #12/6
    "FASTPitot/Data_Files/Mesonet_Data_Files/12_8_2016/GPSLOG09.TXT", #12/8
    "FASTPitot/Data_Files/Irvington_Flight_Tests/12_9_2016/GPS_SOUNDINGS.TXT", #12/9 - 2 soundings at Irvington
    "FASTPitot/Data_Files/Mesonet_Data_Files/12_15_2016/GPSLOGFOUR.TXT", #12/15 - This is the first day I used the FOURPitot sensor
    "FASTPitot/Data_Files/Municipal_Flight_Tests/1_13_2017/FP4.TXT", #1/13/2017
    "", #Rain Date
    ["Compiled_Data/Mesonet_Results/4_13_2017/FP4.TXT","Compiled_Data/Mesonet_Results/4_13_2017/FP4V.TXT"], #4/13
]    
    
sigma_pitot = 0.03 #Closer to 0 means more filtering

##############Mesonet File Name###########

mesonetFiles = [
    "Mesonet/Data_Files/mobileusaw_2016-08-24_2016-08-24.csv", #8/24
    "Mesonet/Data_Files/mobileusaw_2016-08-30_2016-08-30.csv", #8/30
    "Mesonet/Data_Files/mobileusaw_2016-09-06_2016-09-06.csv", #9/6
    "Mesonet/Data_Files/mobileusaw_2016-09-13_2016-09-13.csv", #9/13
    "Mesonet/Data_Files/mobileusaw_2016-09-20_2016-09-20.csv", #9/20
    "Mesonet/Data_Files/mobileusaw_2016-09-27_2016-09-27.csv", #9/27
    "Mesonet/Data_Files/mobileusaw_2016-10-04_2016-10-04.csv", #10/4
    "Mesonet/Data_Files/mobileusaw_2016-10-11_2016-10-11.csv", #10/11
    "Mesonet/Data_Files/mobileusaw_2016-10-18_2016-10-18.csv", #10/18
    "Mesonet/Data_Files/mobileusaw_2016-10-21_2016-10-21.csv", #10/21
    "Mesonet/Data_Files/mobileusaw_2016-10-25_2016-10-25.csv", #10/25
    "Mesonet/Data_Files/mobileusaw_2016-11-01_2016-11-01.csv", #11/1
    "Mesonet/Data_Files/mobileusaw_2016-11-08_2016-11-08.csv", #11/8
    "Mesonet/Data_Files/mobileusaw_2016-11-15_2016-11-15.csv", #11/15
    "Mesonet/Data_Files/mobileusaw_2016-11-22_2016-11-22.csv", #11/22
    "Mesonet/Data_Files/mobileusaw_2016-11-29_2016-11-29.csv", #11/29
    "Mesonet/Data_Files/mobileusaw_2016-12-06_2016-12-06.csv", #12/6
    "Mesonet/Data_Files/mobileusaw_2016-12-08_2016-12-08.csv", #12/8
    "", #12/9 - This was at Irvington
    "Mesonet/Data_Files/mobileusaw_2016-12-15_2016-12-15.csv", #12/15
    "", #1/13/2017 - This was at the Municipal Park
    "Mesonet/Data_Files/mobileusaw_2017-02-07_2017-02-07.csv", #2/7
    "Compiled_Data/Mesonet_Results/4_13_2017/mobileusaw_2017-04-13_2017-04-13.csv", #4/13
]

##############Grab Anemometer Data########

anemometerFiles = [
    "", #8/24
    "", #8/30
    "", #9/6
    "", #9/13
    "", #9/20
    "", #9/27
    "", #10/4
    "", #10/11
    "", #10/18
    "", #10/21
    "", #10/25
    "", #11/1
    "", #11/8
    "", #11/15 - Anemometer not purchased until 11/15 and not implemented until 11/22
    'Anemometer/Data_Files/11_22_2016/GPSLOG09.TXT', #11/22
    'Anemometer/Data_Files/11_29_2016/GPSLOG01.TXT', #11/29
    'Anemometer/Data_Files/12_6_2016/GPSLOG01.TXT', #12/6
    'Anemometer/Data_Files/12_8_2016/GPSLOG02.TXT', #12/8
    "Anemometer/Data_Files/Irvington_Flight_Tests/12_9_2016/GPSLOG03.TXT", #12/9 - Irvington Flight Test
    'Anemometer/Data_Files/12_15_2016/GPSLOG08.TXT', #12/15
    'Anemometer/Data_Files/Municipal_Park_Tests/1_13_2017/GPSLOG09.TXT', #1/13
    "Anemometer/Data_Files/2_7_2017/GPSLOG11.TXT", #2/7
    "Compiled_Data/Mesonet_Results/4_13_2017/ANEM.TXT" #4/13
]

sigma_anemometer = 0.03 #Closer to 0 means more filtering

###############Dates######################

Dates = [
    '8_24_2016', #0
    '8_30_2016', #1
    '9_6_2016', #2
    '9_13_2016', #3
    "9_20_2016", #4
    "9_27_2016", #5
    "10_4_2016", #6
    "10_11_2016", #7
    "10_18_2016", #8
    "10_21_2016", #9
    '10_25_2016', #10
    "11_1_2016", #11
    "11_8_2016", #12
    "11_15_2016", #13
    "11_22_2016", #14
    "11_29_2016", #15
    "12_6_2016", #16
    "12_8_2016", #17
    "12_9_2016", #18
    "12_15_2016", #19
    "1_13_2017", #20
    "2_7_2017", #21
    "4_13_2017", #22
]

###Run the plotting script
#for i in range(0,len(Dates)):
SHOWPLOTS = 0 #1 = show plots, 0 = convert to PDF
i = 22
if True:
    if i > 18:
        numPitots = 4 #on 12_15_2016 I used the FOURPitot sensor
    else:
        numPitots = 1
    quadFile = quadFiles[i]
    iMetFile = iMetFiles[i]
    mesonetFile = mesonetFiles[i]
    anemometerFile = anemometerFiles[i]
    pitotFile = pitotFiles[i]
    ##CAL_TIMES for pitot probe default to 0,20 if you set it to -99
    if i == 19 or i == 20:
        CAL_TIMES = [250,300] #It seems like the pitot probe south needs 300 seconds to warm up - 5 minutes??? Wow.
    elif i == 18 or i == 17:
        CAL_TIMES = [0,100]
    else:
        CAL_TIMES = [-99,0]
    FILES = [quadFile,iMetFile,pitotFile,mesonetFile,anemometerFile]
    do_everything(FILES,sigma_pitot,numPitots,CAL_TIMES,sigma_anemometer,SHOWPLOTS)
    #Rename file
    if sys.platform == 'linux2':
        os.system('cp plots.pdf ' + 'plots_' + Dates[i] + '.pdf')

    # This has been moved to BlackBox/pdf/pdf.py
    # os.system('evince ' + 'plots_' + Dates[i] + '.pdf &')
