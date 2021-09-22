import numpy as np ###This import numeric python
import matplotlib.pyplot as plt ###matlab (matrix laboratory) python plotting hack

truth_value = 9.81
measurements1 = np.loadtxt('Accel_Sensor_Data.txt')

###This creates one big row
#all_measurements = np.concatenate((measurements1,measurements2))

##What if I want two rows? I will look this up later
#matrix = np.vstack((measurements1,measurements2))
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

avg_random_error = np.mean(random_error)
print('Average Random Error = ',avg_random_error)

plt.figure()
plt.plot(random_error)
plt.xlabel('Trials')
plt.ylabel('Random Error (Volts)')
plt.grid()

###Deviation from truth
deviation_from_truth = measurements1-truth_value
plt.figure()
plt.plot(deviation_from_truth)





plt.show()