import numpy as np ###This import numeric python
import matplotlib.pyplot as plt ###matlab (matrix laboratory) python plotting hack

truth_value = 6.11

measurements1 = np.asarray([5.98,6.05,6.10,6.06,5.99,5.96,6.02,6.09,6.03,5.99])
measurements2 = np.asarray([4.98,5.05,7.10,6.16,5.59,5.76,6.32,6.19,6.0,4.99])

###This creates one big row
all_measurements = np.concatenate((measurements1,measurements2))

##What if I want two rows? I will look this up later

###What if I want to manually type in a matrix
#A = np.asarray([[1,2],[2,3]])
#print(A)

###Compute the average
average_measurement = np.mean(measurements1)
print('Average = ',average_measurement)

###Systematic error
sys_error = average_measurement - truth_value
print('Systematic Error = ',sys_error)

###Random Error
### measured_signal - average signal
random_error = measurements1 - average_measurement
print('Random Error = ',random_error)

plt.figure()
plt.plot(random_error)
plt.xlabel('Trials')
plt.ylabel('Random Error (Volts)')
plt.grid()







plt.show()