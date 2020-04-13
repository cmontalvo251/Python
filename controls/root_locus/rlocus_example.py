import numpy as np
import matplotlib.pyplot as plt
import control as ctl

G = ctl.tf([1,3],[1,4,5,0])
H = ctl.tf([1],[1,1])
L = G*H
print(H)
print(G)

ctl.pzmap(L)
ctl.rlocus(L)
plt.show()