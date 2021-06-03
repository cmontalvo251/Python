import numpy as np
import matplotlib.pyplot as plt

a = np.linspace(-20,20,1000)

y = -(18*a - 25*a - 15*a**2)

plt.plot(a,y)
plt.grid()
plt.show()