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
#Convert to Atmospheres
deltaP_kPa = deltaV
deltaP_Pa = deltaP_kPa * 1000.
deltaP_atm = deltaP_kPa/101.325

plt.figure()
plt.plot(time,voltage)
plt.figure()
plt.plot(time,deltaV)

###What is the equation to get to windspeed?

##There are two
## V1 = 2*dP_Pa/density
density = 1.225 #kg/m^3
V1 = np.sqrt(2*deltaP_Pa/density)

##The incompressibility equation
a0 = 331.0 #speed of sound at sea-level
k = 5*((deltaP_atm+1)**(2.0/7.0)-1)
k[k<0]=0
V2 = a0*np.sqrt(k)

##Let's add a complimentary filter
V2_filtered = 0*V2
s = 0.9
for i in range(0,len(V2)-1):
    V2_filtered[i+1] = V2_filtered[i]*s + (1-s)*V2[i]

plt.figure()
plt.plot(time,V1,label='Incompressible')
plt.plot(time,V2,label='Compressible')
#plt.plot(time,V2_filtered,label='Filtered Windspeed')
plt.xlabel('Time (sec)')
plt.ylabel('Windspeed (m/s)')
plt.grid()
plt.legend()
plt.show()



#plt.figure()
#plt.plot(time,V1)
#plt.title('Windspeed vs. Time')
#plt.xlabel('Time (sec)')
#plt.ylabel('Windspeed(m/s)')
#plt.grid(1)
#plt.show()
