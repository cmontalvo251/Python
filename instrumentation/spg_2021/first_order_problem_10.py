import numpy as np
import matplotlib.pyplot as plt

time = np.asarray([0.1,0.5,1,2,3])
temp = np.asarray([16.7,8.1,3.3,0.6,0.1])

plt.plot(time,temp,'b*')

##Settling
tsettle = 2.0
time_constant = 4.0/tsettle

temp_analytic = temp[0]*np.exp(-time_constant*time)

plt.plot(time,temp_analytic,'r-')

plt.show()