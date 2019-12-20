from numpy import *
from matplotlib.pyplot import *
from scipy.integrate import *

close("all")

def Derivatives(v,t):
    #Proportional Control
    kp = 25
    vtilde = v ##Assuming perfect measurement
    vc = 31.3
    e = vc - vtilde
    throttle = kp*e ##Infinite control input
    if throttle > 100:
        throttle = 100
    horsepower = 545
    power = 745.7*horsepower*throttle/100
    m = (2000)/2.2
    force = power/v
    if force > 1000:
        force = 1000
    density = 1.225
    S = 2.0 #square meters
    CD = 0.26
    Drag = 0.5 * density * v**2 * S * CD
    vdot = -Drag/m + force/m
    return vdot
    
tout = linspace(0,50,1000)
vinitial = 0
vout = odeint(Derivatives,vinitial,tout)

plot(tout,vout)

grid()
xlabel('Time (sec)')
ylabel('Velocity (m/s)')
show()