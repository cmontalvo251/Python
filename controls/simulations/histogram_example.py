import numpy as np
import matplotlib.pyplot as plt
import statistics as s
bin_width = 0.2
x = np.array([49.3,50.1,49.3,50.5,48.9])
number_of_bins = int((np.max(x) - np.min(x))/bin_width)
print(number_of_bins)
plt.hist(x,bins=number_of_bins)
print(np.median(x))
print(s.mode(x))
plt.show()