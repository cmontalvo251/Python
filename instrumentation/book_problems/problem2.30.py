import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('data.txt',delimiter=',')

true_force = data[:,0]
measured_mV = data[:,[1,2,3,4,5]]

plt.figure()
plt.plot(true_force,measured_mV,'r*')
plt.grid()

##Fit a trend line
coeff = np.polyfit(true_force,measured_mV,1) #0 = flat, 1 = linear, 2 = quadratic

fitted_line = np.linspace(0,100,100)

slopes = coeff[0]
intercepts = coeff[1]

average_slope = np.mean(slopes)
average_intercept = np.mean(intercepts)

coeff_average = [average_slope,average_intercept]

fitted_line_y = np.polyval(coeff_average,fitted_line)

plt.plot(fitted_line,fitted_line_y)

plt.show()