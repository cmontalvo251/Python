import control as ctl
import numpy as np
import matplotlib.pyplot as plt

plt.close("all")

g= 9.81
L = 2.0
wn = np.sqrt(g/L)
G = ctl.tf([1],[1,0,wn**2])
print(G)

C = ctl.tf([1,1],[1,100])
print(C)

ctl.bode(C*G,dB=True)
plt.grid()

`gm,pm,wg,wp = ctl.margin(C*G)

print(gm,pm,wg,wp)

ctl.rlocus(C*G)

plt.show()
