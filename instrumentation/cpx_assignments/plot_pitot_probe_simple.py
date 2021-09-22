import numpy as np
import matplotlib.pyplot as plt
 
data = np.loadtxt('Pitot.txt')
time = data[:,1]
Do = data[:,0]*65536/3.3 ##number between 0 and 65536 - 

##Plot raw digital output
plt.figure()
plt.plot(time,Do)
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Digital Output of ADC')

##Convert to voltage
voltage = Do*3.3/65536
##Bias the voltage
Vbias = 49720.*3.3/65536.
##DeltaV
deltaV = voltage - Vbias
deltaV[deltaV<0]=0.0
#Convert to Atmospheres
deltaP_kPa = deltaV
deltaP_Pa = deltaP_kPa * 1000.
density = 1.225 #kg/m^3
U = np.sqrt(2*deltaP_Pa/density)

U_filtered = 0*U
ctr = 0
s = 0.2
for ui in U:
    if ctr < len(U)-1:
        U_filtered[ctr+1] = U_filtered[ctr]*(1-s) + ui*s
    ctr+=1

plt.figure()
plt.plot(time,U,label='Raw Signal')
plt.plot(time,U_filtered,label='Filtered Signal')
plt.xlabel('Time (sec)')
plt.ylabel('Windspeed (m/s)')
plt.grid()
plt.legend()
plt.show()