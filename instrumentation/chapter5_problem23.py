import matplotlib.pyplot as plt
import numpy as np

t_truth = np.arange(0.00025,0.1,0.000001)

t = np.arange(0.00025,0.1,1.0/400.0)

f = 3*np.cos(500*np.pi*t) + 5*np.cos(800*np.pi*t)

f_truth = 3*np.cos(500*np.pi*t_truth) + 5*np.cos(800*np.pi*t_truth)

plt.plot(t_truth,f_truth,'b-')
plt.plot(t,f,'r-*')

plt.show()
