import numpy as np
import matplotlib.pyplot as plt
import control as ctl

G = ctl.tf([1],[1,0,0])
C = ctl.tf([1],[1,10])
C2 = ctl.tf([1,3],[1,10])

print(C)
print(C2)
print(G)

ctl.rlocus(G)
ctl.rlocus(C*G)
ctl.rlocus(C2*G)

plt.show()