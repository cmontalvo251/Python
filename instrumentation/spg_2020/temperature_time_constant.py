import numpy as np
import matplotlib.pyplot as plt

cool = np.loadtxt('Cool_Down.txt')
heat = np.loadtxt('Heat_Up.txt')

time_cool = cool[:,0]
temp_cool = cool[:,1]
plt.figure()
plt.plot(time_cool,temp_cool,'b*',label='Measured Data')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (C)')

###Time Constant
t0 = 77.831
TsC = 720-t0
tauC = 4./TsC
Ta = -8.44
T0 = 26.5
time_cool_sim = np.linspace(0,time_cool[-1]-t0,1000)
temp_cool_sim = (Ta-T0)*(1-np.exp(-tauC*time_cool_sim)) + T0
plt.plot(time_cool_sim+t0,temp_cool_sim,'r-',label='Fitted Data')
plt.legend()

time_heat = heat[:,0]
temp_heat = heat[:,1]
plt.figure()
plt.plot(time_heat,temp_heat,'b*',label='Measured Data')
plt.grid()
plt.xlabel('Time (sec)')
plt.ylabel('Temperature (C)')

t0 = 4.94
TsH = 350-t0
tauH = 4./TsH
Ta = 25.33
T0 = -1.03
time_heat_sim = np.linspace(0,time_heat[-1]-t0,1000)
temp_heat_sim = (Ta-T0)*(1-np.exp(-tauH*time_heat_sim)) + T0
plt.plot(time_heat_sim+t0,temp_heat_sim,'r-',label='Fitted Data')
plt.legend()



plt.show()