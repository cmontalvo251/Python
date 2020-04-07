import numpy as np
import matplotlib.pyplot as plt

a = np.linspace(-20,20,1000)

y = -(180000*a - 2500*a - 15000*a**2)

plt.plot(a,y)
plt.grid()
plt.show()