import numpy as np
import matplotlib.pyplot as plt
mu = 10.0
stddev = 1.0
def f(x):
    return 1/(stddev*np.sqrt(2*np.pi))*np.exp(-(x-mu)**2/(2*stddev**2))
lim = 4.0
x = np.linspace(mu-lim*stddev,mu+lim*stddev,1000)
plt.plot(x,f(x))
plt.grid()
##I want to draw 95% confidence
#from table 6.3 in instrumentation
zval = 1.96
xvalUpper = mu + zval*stddev
xvalLower = mu - zval*stddev
print('95% Confidence = ',xvalLower,xvalUpper)
fL = f(xvalLower)
fU = f(xvalUpper)
plt.plot([xvalUpper,xvalUpper],[0,np.max(f(x))],'r-')
plt.plot([xvalLower,xvalLower],[0,np.max(f(x))],'r-')
plt.show()