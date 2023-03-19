import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sci

def f(x):
    return 5*x**3-20*x

###Find Zeros using Fsolve
guesses = np.linspace(-5,5,10)
roots = []
for guess in guesses:
    root = sci.fsolve(f,guess)
    roots.append(root[0])

##Only grab unique roots
print(np.unique(roots))
x = np.linspace(-10,10,100)
y = f(x)
plt.plot(x,y)
plt.grid()
plt.show()