import numpy as np
import matplotlib.pyplot as plt

##This is a comment
##Let's make a vector of x
x = np.linspace(-10,10,1000) ##This will make a vector x that starts at -10 and end
##############.42#at 10 and uses 20 data points
#print('x=',x)

###Let's compute y = x**2
y = x**2
y2 = 100*np.sin(x)
#print('y=',y)

plt.plot(x,y,label='First plot')
plt.plot(x,y2,label='Second plot')
plt.grid()
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.title('This is a f*#$king sick plot')
plt.show()

