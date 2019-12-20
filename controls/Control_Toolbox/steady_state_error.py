###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as ctl
import scipy.signal as S
import scipy.linalg as slin

plt.close("all")
####Zeros Poles and Gains
###Zeros are the roots of the numerator
####Poles are the roots of the denominator
####Gain is the leading coefficient of numerator/leading coefficient of the denominator
zeros = []
poles = [-3.0]
gain = 3.0
[N,D] = S.zpk2tf(zeros,poles,gain)
G = ctl.tf(N,D)

tout = np.linspace(0,5,1000)

tout,yout = ctl.step_response(G,tout)

zeros = []
poles = 0
gain = 2.0
[N,D] = S.zpk2tf(zeros,poles,gain)
C = ctl.tf(N,D)

sys_closed_loop = C*G/(1+C*G)

toutc,youtc = ctl.step_response(sys_closed_loop,tout)

plt.plot(tout,yout,'r-',label='Open Loop')
plt.plot(tout,youtc,'g-',label='Closed Loop')
plt.xlabel('Time (sec)')
plt.ylabel('State')
plt.legend()
plt.grid()
plt.show()