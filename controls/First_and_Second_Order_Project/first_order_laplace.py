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

###Experimental Data
ydata = [0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0,
0.3885754595,
0.3497179135,
0.7033215817,
1.1088911257,
1.4739037154,
1.6012800529,
1.4411520476,
1.7729385451,
1.5956446906,
1.4360802215,
1.7683739016,
2.2059123846,
2.6583303993,
3.2613186426,
3.8464063817,
3.4617657436,
3.5914908715,
3.7818610033,
3.7922503625,
3.9625445452,
4.042191793,
4.0265480732,
4.296902519,
4.2557877265,
4.6544522915,
4.9661178251,
5.2937493801,
5.3138936611,
5.332023514,
4.7988211626,
4.3189390464,
4.7112884793,
4.7896788504,
4.7866126676,
5.1767726841]


xdata = np.asarray([2,
2.22,
2.42,
2.62,
2.82,
3.02,
3.22,
3.43,
3.63,
3.83,
4.03,
4.23,
4.43,
4.63,
4.83,
5.03,
5.23,
5.43,
5.63,
5.83,
6.03,
6.23,
6.44,
6.64,
6.84,
7.04,
7.24,
7.44,
7.64,
7.84,
8.04,
8.24,
8.44,
8.64,
8.84,
9.05,
9.25,
9.45,
9.65,
9.85,
10.05,
10.25,
10.45,
10.65,
10.85,
11.05,
11.25,
11.45,
11.65,
11.86])


plt.plot(xdata-5,ydata,'b*',label='Experimental Data')

###Zeros poles and gains
# X = k / (s + c)
c = 0.5
k = 0.02
N = [120*k]
D = [1,c]
sys = ctl.tf(N,D)
print sys
tout = np.linspace(0,10,1000)
tout,yout = ctl.step_response(sys,tout)
plt.plot(tout,yout,'g--',label='Simulation')
plt.xlabel('Time (sec)')
plt.ylabel('Measured Windspeed (m/s)')
plt.legend()
plt.grid()
plt.show()