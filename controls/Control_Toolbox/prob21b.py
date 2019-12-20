import control as ctl
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as S

plt.close("all")

[N,D] = S.zpk2tf([-3./2.],[-1,-1],[-2])
sys1 = ctl.tf(N,D)
sys1_alt = ctl.tf([-2,-3],[1,2,1])

print sys1,sys1_alt

[N,D] = S.zpk2tf([],[-2,-1,-1],[5])
sys2 = ctl.tf(N,D)
sys2_alt = ctl.tf([5],[1,4,5,2])

print sys2,sys2_alt

[N,D] = S.zpk2tf([],[-1,-1,0,0],[1])
sys3 = ctl.tf(N,D)
sys3_alt = ctl.tf([1],[1,2,1,0,0])

print sys3,sys3_alt

sys = sys1 + sys2 + sys3

sys_alt = ctl.tf([1],[1,2,1,0,0]) + ctl.tf([5],[1,4,5,2]) + ctl.tf([-2,-3],[1,2,1])

print sys,sys_alt

tout = np.linspace(0,10,100)

[tout,yout] = ctl.impulse_response(sys,tout)

plt.plot(tout,yout)
plt.grid()
plt.show()