import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

data = np.loadtxt('Test_Data.txt',delimiter=' ')

print(np.shape(data))

time = data[:,0]

gravity = data[:,3]

plt.plot(time,gravity)

gravity_mean = np.mean(gravity)
gravity_standard_dev = np.std(gravity)
gravity_mode = stats.mode(gravity)
variance = gravity_standard_dev**2
print(gravity_mean)
print(gravity_standard_dev)
print(gravity_mode)
print(variance)
sorted = np.sort(gravity)
print('Median = ',sorted[int(len(sorted)/2.)])
median = np.median(gravity)
print('Stats Median = ',median)
plt.figure()
plt.hist(gravity)

plt.show()