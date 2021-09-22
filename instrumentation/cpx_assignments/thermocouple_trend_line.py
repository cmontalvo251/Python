import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

###Could put this in by hand
T = np.asarray([20,30,40,50,60,75,100])
mV = np.asarray([1.02,1.53,2.05,2.55,3.07,3.56,4.05])

##Lists cannot do math operations
#Tlist = [10,20]

###Could also put data into a text file and then 
#data = np.loadtxt('thermocouple_data.txt')
#Tdata = data[:,0]
#mVdata = data[:,1]


###Linear Trend Line
coeff = np.polyfit(mV,T,2) ##mv is X, T is y and 1 is linear (2 = quadratic)
print(coeff)

####Evaluate the trend line to plot a "continuous" line
mVfit = np.linspace(np.min(mV),np.max(mV),1000)
Tfit = np.polyval(coeff,mVfit)



###let's compute residuals
ybar = np.mean(T)
Ti = np.polyval(coeff,mV)
res = Ti - T
rsquared = 1 - np.sum(res**2)/np.sum((T-ybar)**2)

print('R^2 = ',rsquared)

plt.plot(mV,T,'b*',label='Experimental Data')
plt.plot(mVfit,Tfit,'r-',label='Polynomial Fit') ### 'r-' is a red line 'k-' black line 'c--' cyan dashed line
plt.plot(mV,Ti,'gs',label='Data Evaluated at Trend Line')
plt.legend()

plt.figure()
plt.plot(mV,res,'b*')

plt.show()
