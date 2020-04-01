import matplotlib.pyplot as plt
import numpy as np

data = [49.3,50.1,48.9,49.2,49.3,50.5,49.9,49.2,49.8,50.2]

plt.figure()
plt.plot(data,'b*')

bins = np.arange(np.min(data),np.max(data),0.1)

plt.figure()
plt.hist(data,bins)
plt.grid()


plt.show()