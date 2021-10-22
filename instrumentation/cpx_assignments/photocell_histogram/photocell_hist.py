import numpy as np
import matplotlib.pyplot as plt

###IMPORT DATA
data = np.loadtxt('Ambient_Light_Conditions.txt')

###GRAB TIME
time = data[:,0]
###SHIFT TIME TO ZERO
time -= time[0]
##CONVERT DATA TO VOLTAGE
voltage = data[:,1]*3.3/2**16

###THROW OUT BAD TIME SERIES
voltage = voltage[time>161]
time = time[time>161]

###THROW OUT OUTLIERS
##COMPUTE CURRENT MEAN AND DEV
mean = np.mean(voltage)
dev = np.std(voltage)
print(mean,dev)
time = time[voltage > mean - 3*dev]
voltage = voltage[voltage > mean - 3*dev]
time = time[voltage < mean + 3*dev]
voltage = voltage[voltage < mean + 3*dev]

###COMPUTE NEW MEAN,STD
mean = np.mean(voltage)
dev = np.std(voltage)
print(mean,dev)

###COMPUTE THE NORMAL DISTRIBUTION
x = np.linspace(mean-3*dev,mean+3*dev,1000)
dx = x[1]-x[0]
N = len(voltage)
fx = (1/(np.sqrt(2*np.pi)*dev))*np.exp(-(x-mean)**2/(2*dev**2))*dx*N*100

###PLOT TIME SERIES
plt.plot(time,voltage,'b*')
plt.xlabel('Time (sec')
plt.ylabel('Photocell Voltage (V)')
plt.grid()
###PLOT HISTOGRAM
plt.figure()
plt.hist(voltage,bins=18)
plt.plot(x,fx)
plt.xlabel('Voltage (V)')
plt.ylabel('Number of Occurences')
plt.grid()

plt.show()