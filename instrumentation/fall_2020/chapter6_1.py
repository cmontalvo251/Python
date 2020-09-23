import numpy as np
import matplotlib.pyplot as plt

###Readings
readings = np.asarray([49.3,50.1,48.9,49.2,49.3,50.5,49.9,49.2,49.8,50.2])

###Mean, Stdev
mean = np.mean(readings)
median = np.median(readings)
stddev = np.std(readings)
print('Mean = ',mean)
print('Median = ',median)
print('Stdev = ',stddev)
print('Number of Readings = ',len(readings))

###Make a histogram
plt.hist(readings,bins=10)
plt.xlabel('Distance (cm)')
plt.ylabel('Count')
plt.grid()
plt.show()

