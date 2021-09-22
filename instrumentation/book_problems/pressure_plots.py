import numpy as np
import matplotlib.pyplot as plt

pressure = np.asarray([20.0,40.4,60.8,80.2,100.4,120.3,141.1,161.4,181.9,201.4,220.8,241.8,261.1,280.4,300.1,320.6,341.1,360.8])
temperature = np.asarray([44.9,102.4,142.3,164.8,192.2,221.4,228.4,249.5,269.4,270.8,291.5,287.3,313.3,322.3,325.8,337,332.6,342.9])

coeff = np.polyfit(pressure,temperature,3)
print(coeff)

pressure_fit = np.linspace(pressure[0],pressure[-1],1000)
temperature_fit = np.polyval(coeff,pressure_fit)

vals = np.polyval(coeff,pressure)
residuals = temperature - vals

##Correlation coefficient
mean_temperature = np.mean(temperature)
s = np.sum(residuals**2)/np.sum((temperature-mean_temperature)**2)
r2 = 1 - s
print(r2)

plt.plot(pressure,temperature,'b*')
plt.plot(pressure_fit,temperature_fit,'r-')
plt.xlabel('Pressure (psia')
plt.ylabel('Temperature (F)')
plt.grid()

plt.figure()
plt.plot(residuals,'b*')
plt.grid()
plt.show()
