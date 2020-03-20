import control as ctl #Control systems toolbox
import matplotlib.pyplot as plt #plotting toolbox
import numpy as np #numeric python toolbox

##Constants
A = 5.
B = 6.
a = 2.
ro = 15.
wo = -3.

##Transfer Functions
Hy = a/A
G = ctl.tf([A],[1,a])
print(G)
D = ctl.tf([B],[1,a])
print(D)

##Design My Command Generation Block
Hr = Hy

##Design my controller
kp = 100
print('kp=',kp)
C = kp

GOL = Hr*1*G ##let kp = 1 so we can compare apples to apples
print(GOL)

tout = np.linspace(0,10,1000)

tout,xout = ctl.step_response(GOL,tout) ##assumed that r = 1

tout,wdout = ctl.step_response(D,tout)

#scale wdout by wo
wdout *= wo

##scale the output by r = ro
xout *= ro

yout = wdout + xout

##Close the loop without a disturbance
GDEN = 1/(1+C*G*Hy)

tout,xoutCL = ctl.step_response(Hr*C*G*GDEN,tout)

tout,wdoutCL = ctl.step_response(D*GDEN,tout)

#scale the output
wdoutCL *= wo

#scale by ro
xoutCL *= ro

youtCL = xoutCL + wdoutCL

plt.figure()
plt.plot(tout,xoutCL,label='Closed Loop No Disturbance')
plt.plot(tout,youtCL,label='Closed Loop with Disturbance')
plt.plot(tout,xout,label='Open Loop No Disturbance')
plt.plot(tout,yout,label='Open Loop With Disturbance')
plt.grid()
plt.legend()
plt.xlabel('Time (sec')
plt.ylabel('Speed (m/s)')

plt.show()
