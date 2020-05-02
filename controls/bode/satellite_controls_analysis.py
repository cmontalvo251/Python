import control as ctl
import matplotlib.pyplot as plt
import numpy as np

###Inertia Calculation
a = 10/100.
m = 3
I = (m/12.)*(a**2+a**2)
print(I)
###Plant Dynamics
G = ctl.tf([1],[0.003,0,0])
print(G)

###Actuator Dynamics
time_constant = 1/1.316
sig = 1/time_constant
A = ctl.tf([sig],[1,sig])
print(A)

###Sensor Dynamics
time_constantH = 1/1000.
sigH = 1/time_constantH
H = ctl.tf([sigH],[1,sigH])
print(H)

###Open Loop System
GOL = A*G*H

ctl.bode(GOL)

##Design your compensator
C = ctl.tf([1],[1,1])
print(C)

###Plant with Compensation
GC = C*GOL
ctl.bode(GC)


plt.show()
