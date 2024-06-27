import numpy as np
import matplotlib.pyplot as plt

##I am going to make this code general for any system
x_axis = np.array([1.02,1.53,2.05,2.55,3.07,3.56,4.05])
y_axis = np.array([20,30,40,50,60,75,100])

##Use poly functions to fit the data
coeff = np.polyfit(x_axis,y_axis,1)
print(coeff)

##Make a bunch of data points
x_fit = np.linspace(np.min(x_axis),np.max(x_axis),50000000)
#print(x_fit)
y_fit = np.polyval(coeff,x_fit)
y_data = np.polyval(coeff,x_axis)


#First let's just plot
plt.plot(x_axis,y_axis,'b*')
plt.plot(x_fit,y_fit,'r-')
plt.plot(x_axis,y_data,'r*')
plt.grid()

##Plot the residuals
res = y_axis - y_data
plt.figure()
plt.plot(x_axis,res,'b*')
plt.grid()

#Also compute the coefficient of determination
r2 = 1 - np.sum((y_data - y_axis)**2)/np.sum((y_axis - np.mean(y_axis))**2)
print('Coefficient of Determination = ',r2)
rcorrelation = np.corrcoef(x_axis,y_axis)
print('Correclation Coefficient = ',rcorrelation[0][1])
plt.show()