import numpy as np
import matplotlib.pyplot as plt

##DATA
us = np.array([680,750,1200,1800,2000])
theta = np.array([11,45,92,135,179])

###USE POLYFIT TO FIT A LINE
coeff = np.polyfit(theta,us,1) #1 for linear, 2 for quadratic, etc...
print(coeff)

###PLOT TRENDLINE
thetatrend = np.linspace(np.min(theta),np.max(theta),1000)
ustrend = np.polyval(coeff,thetatrend)

##COMPUTE OUTPUT OF TRENDLINE AT XVALUES
Ytilde = np.polyval(coeff,theta)

plt.plot(theta,us,'b*')
plt.plot(thetatrend,ustrend,'r-')
plt.plot(theta,Ytilde,'g*')
plt.xlabel('Degrees')
plt.ylabel('Microseconds')
plt.grid()

###COMPUTE RESIDUALS
res = (us-Ytilde)**2

plt.figure()
plt.plot(theta,res,'b*')
plt.xlabel('Degrees')
plt.ylabel('Residuals Squared')
plt.grid()

###R^2
R2 = 1 - np.sum(res) / np.sum((us-np.mean(us))**2)
print('R2 = ',R2)


plt.show()