import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('Weight_Data_Example.txt')

known_weight = data[:,0]
measured_weight = data[:,1]

plt.figure()
plt.plot(data[:,0],data[:,1],'r*')
plt.grid()

##Fit a trend line
coeff = np.polyfit(known_weight,measured_weight,1)

fitted_line = np.linspace(0,5,100)
fitted_line_y = np.polyval(coeff,fitted_line)

plt.plot(fitted_line,fitted_line_y)

plt.show()