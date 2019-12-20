import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

data = []
for x in range(0,1000):
    data.append(np.random.normal())

print(data)

plt.plot(data)
plt.grid()

plt.figure()
plt.hist(data)

print('Mean = ',np.mean(data))
print('Mode = ',stats.mode(data)) #Returns most common value this does not work for continuous sampling points
sorted = np.sort(data)
print('Mode = ',sorted[int(len(sorted)/2.)])

plt.show()