import numpy as np
import matplotlib.pyplot as plt

##DATA
ms = np.array([680,750,1200,1800,2000])/1000.0
theta = np.array([11,45,92,135,179])

###USE POLYFIT TO FIT A LINE
coeff = np.polyfit(theta,ms,1) #1 for linear, 2 for quadratic, etc...
print(coeff)

###PLOT TRENDLINE
thetatrend = np.linspace(np.min(theta),np.max(theta),1000)
mstrend = np.polyval(coeff,thetatrend)

##COMPUTE OUTPUT OF TRENDLINE AT XVALUES
Ytilde = np.polyval(coeff,theta)

plt.plot(theta,ms,'b*')
plt.plot(thetatrend,mstrend,'r-')
plt.plot(theta,Ytilde,'g*')
plt.xlabel('Degrees')
plt.ylabel('Milli Seconds')
plt.grid()

###COMPUTE RESIDUALS
res = (ms-Ytilde)**2

plt.figure()
plt.plot(theta,res,'b*')
plt.xlabel('Degrees')
plt.ylabel('Residuals Squared')
plt.grid()

###R^2
R2 = 1 - np.sum(res) / np.sum((ms-np.mean(ms))**2)
print('R2 = ',R2)


plt.show()