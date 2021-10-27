import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 22})

T = np.array([20,30,40,50,60,75,100])
V = np.array([1.02,1.53,2.05,2.55,3.07,3.56,4.05])

coeff = np.polyfit(V,T,2)
print(coeff)

plt.plot(V,T,'b*',markerSize=10)

Vtrend = np.linspace(V[0],V[-1],100)

###THIS BELOW ONLY WORKS IF YOU ARE FITTING A LINEAR TREND LINE
#Ttrend = coeff[0]*Vtrend + coeff[1]
Ttrend = np.polyval(coeff,Vtrend)

###Residuals
Tatdatapts = np.polyval(coeff,V)
residuals = (Tatdatapts - T)**2

plt.plot(Vtrend,Ttrend,'r-',LineWidth=2)
plt.plot(V,Tatdatapts,'r*',MarkerSize=10)

plt.xlabel('V(mV)')
plt.ylabel('T(C)')
plt.grid()


plt.figure()
plt.plot(V,residuals,'b*')
plt.grid()

mean = np.mean(Tatdatapts)
r2 = 1 - np.sum(residuals)/np.sum((Tatdatapts-mean)**2)
print(r2)
plt.show()