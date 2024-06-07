import numpy as np
import matplotlib.pyplot as plt

##PLOT RAW DATA
data = np.loadtxt('pulse.txt',delimiter=',')
Do = data[:,0]
time = data[:,1]
time -= time[0]

##Take a derivative
ddt_Do = (Do[1:] - Do[0:-1])/(time[1:] - time[0:-1])

###PRETEND THAT THE DATA IS BEING SENT TO US IN
###REALTIME - THIS WAY WE CAN COPY CODE TO THE
###CPX EASILY
plt.figure()
signddt = 1.0
prev_time_monotonic = -1
prev_analog_value = 20000.
time_zero_crossings = []
Do_zero_crossings = []
first_peak_time = -1e20
Do_peak_value_avg = 0
Do_peak_value_standard_deviation = 0
for i in range(0,len(time)-2):
    ###ANIMATION SCRIPT
    plt.cla()
    plt.plot(time[0:i],Do[0:i])
    plt.xlim([0,time[-1]])
    plt.ylim([np.min(Do),np.max(Do)])
    plt.grid()
    plt.plot(time_zero_crossings,Do_zero_crossings,'b*')
    plt.pause(0.001)
    
    
###########################################################################################
    
    ##REPLICATE CPX
    
    ##READING THE CURRENT TIME AND Do
    time_monotonic = time[i]
    analog_value = Do[i]
    
    ##TAKE A DERIVATIVE
    ddt_Do = (analog_value - prev_analog_value) / (time_monotonic - prev_time_monotonic)
    prev_analog_value = analog_value
    prev_time_monotonic = time_monotonic
    
    ###FIND ZERO CROSSING
    if signddt > 0 and np.sign(ddt_Do) <= 0:
        second_peak_time = time_monotonic
        ##CHECK FOR APPROPRIATE BPM
        if (second_peak_time - first_peak_time) > 0.2:
            #CHECK FOR FALSE PEAK
            if analog_value > Do_peak_value_avg - 0.8*Do_peak_value_standard_deviation:
                ###PEAK FOUND TIME TO UPDATE VALUES
                time_zero_crossings.append(time_monotonic)
                Do_zero_crossings.append(analog_value)
                Do_peak_value_avg = np.mean(Do_zero_crossings)
                Do_peak_value_standard_deviation = np.std(Do_zero_crossings)
                ##COMPUTE BPM
                delta_time = second_peak_time - first_peak_time
                BPM = 60./delta_time
                print('BPM = ',BPM,'Time = ',time_monotonic,Do_peak_value_avg,Do_peak_value_standard_deviation,analog_value)
                first_peak_time = second_peak_time

    signddt = np.sign(ddt_Do)
    
    #########################################################################
        
##Convert to numpy arrays
time_zero_crossings = np.array(time_zero_crossings)
Do_zero_crossings = np.array(Do_zero_crossings)
 
##PLOT RAW DATA
plt.plot(time,Do)
plt.plot(time_zero_crossings,Do_zero_crossings,'b*')
plt.xlabel('Time (sec)')
plt.ylabel('Do (16 bit)')
plt.grid()

##PLOT DERIVATIVE
#plt.figure()
#plt.plot(time[0:-1],ddt_Do)
#plt.grid()
#plt.xlabel('Time (sec)')
#plt.ylabel('Do dot (Do/sec)')

plt.show()