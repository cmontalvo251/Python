import control as ctl
import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

###Open loop transfer function
N = 3
D = [1,4,4]
sys = ctl.tf(N,D)

print sys

tout = np.linspace(0,30,1000)

tout,dalfaout = ctl.step_response(sys,tout)

alfa0 = 3.
alfaout = dalfaout + alfa0

plt.plot(tout,alfaout,label='Open Loop')

###Closed Loop Transfer Function
kp = 15
kd = 7.5
ki = 25.
N = [3*kd,3*kp,3*ki]
D = [1,(4+3*kd),(4+3*kp),3*ki]
sys_CL = ctl.tf(N,D)

print sys_CL


###alfacommand = 5
###dalfacommand = 5-alfa0 = 2
dalfacommand = 2.
tout,dalfaout = ctl.step_response(sys_CL*dalfacommand,tout)

alfaout = dalfaout + alfa0

plt.plot(tout,alfaout,label='Close Loop')
plt.grid()
plt.legend()

plt.show()