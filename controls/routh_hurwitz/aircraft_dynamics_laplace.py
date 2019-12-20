import control as C
import matplotlib.pyplot as plt
import numpy as np

g = 9.81

G = C.tf([4*g,4*g],[1,4,4,0,0])

kp = 0.5
kd = 0.25

ctrl = C.tf([kd,kp],[])

GCL = G*ctrl/(1+G*ctrl)

tout,xout = C.step_response(CCL,tout)

plt.figure()
plt.plot(tout,xout)

plt.show()