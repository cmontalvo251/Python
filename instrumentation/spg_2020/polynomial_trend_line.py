###Import modules
import numpy as np
import matplotlib.pyplot as plt

###Data Vectors
T = [20,30,40,50,60,75,100]
V = [1.02,1.53,2.05,2.55,3.07,3.56,4.05]

###Plot data
plt.plot(V,T,'b*')
plt.xlabel('Voltage (V)')
plt.ylabel('Temp (C)')
plt.grid()

###Compute the trend line
coeff = np.polyfit(V,T,2) ## 1 = linear
print(coeff)


###Let's plot a trend line
Vtrend = np.linspace(V[0],V[-1],100)
Ttrend = np.polyval(coeff,Vtrend)

plt.plot(Vtrend,Ttrend,'r-')

###let's compute residuals
V = np.asarray(V)
Ttilde = np.polyval(coeff,V)
print(T)
print(Ttilde)
plt.plot(V,Ttilde,'g*')

residuals = Ttilde-T

###Plot residuals
plt.figure()
plt.plot(V,residuals,'b*')
plt.grid()

###Compute r^2
r2 = 1 - np.sum(residuals**2)/np.sum((T-np.mean(T))**2)
print(r2)

plt.show()
