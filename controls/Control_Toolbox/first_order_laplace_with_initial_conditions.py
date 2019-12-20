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

###Zeros poles and gains
# X = (72s + 120k) / s*(s + c)
c = 0.5
k = 0.5
N = [72,120*k]
D = [1,c]
sys = ctl.tf(N,D)
print sys
tout = np.linspace(0,10,1000)
tout,yout = ctl.step_response(sys,tout)
###^The above is using step. vvv Below is using impulse
# X = (72s + 120k) / s*(s + c)
N = [-72,120*k]
D = [1,c,0]
sys2 = ctl.tf(N,D)
print sys2
tout,yout2 = ctl.impulse_response(sys2,tout)

####Zeros Poles and Gains
###Zeros are the roots of the numerator
####Poles are the roots of the denominator
####Gain is the leading coefficient of numerator/leading coefficient of the denominator
zeros = -60.0/72.0
poles = -0.5
gain = 72.0
[N,D] = S.zpk2tf(zeros,poles,gain)
sys3 = ctl.tf(N,D)
print sys3
plt.plot(tout,yout2,'r-',label='Impulse Response')
plt.plot(tout,yout,'g--',label='Step Response')
plt.xlabel('Time (sec)')
plt.ylabel('Temp (F)')
plt.legend()
plt.grid()
plt.show()