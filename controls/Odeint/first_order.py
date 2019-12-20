from numpy import *
from matplotlib.pyplot import *
from scipy.integrate import *

close("all")

def Derivatives(x,t):
    xdot = 5*cos(2*t)-7*x
    return xdot
    
tout = linspace(0,10,1000)
xinitial = 0
xout = odeint(Derivatives,xinitial,tout)

plot(tout,xout,label='Numerical')

matrix = asarray([[-2,7],[7,2]])
sol = asarray([0,5])
BC = matmul(linalg.inv(matrix),sol)
B = BC[0]
C = BC[1]

A = -B
xa = A*exp(-7*tout) + B*cos(2*tout) + C*sin(2*tout)

line,= plot(tout,xa,color='red',label='Analytical')
line.set_dashes([2,2])
legend(loc='upper left')
grid()
xlabel('Time (sec)')
ylabel('Position (m)')
show()
