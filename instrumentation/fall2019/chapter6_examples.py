import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy import stats

data = np.asarray([49.3,50.1,48.9,49.2,49.3,50.5,49.9,49.2,49.8,50.2])

b = np.arange(np.min(data),np.max(data),0.2)

plt.hist(data,bins=b)

mean = np.mean(data)
mode = stats.mode(data)
median = np.median(data)
dev = np.std(data) 

plt.show()