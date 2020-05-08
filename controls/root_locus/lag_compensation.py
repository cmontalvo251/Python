import control as ctl
import numpy as np
import matplotlib.pyplot as plt

wn = 4.6/3.
zed = 1.0
m = 50.
k = 2.*m*zed*wn
a = wn**2 * m/k

print(k,a)

C = ctl.tf([k,k*a],[1])
print(C)

G = ctl.tf([1],[m,0,0])
print(G)

ctl.rlocus(C*G)

plt.show()