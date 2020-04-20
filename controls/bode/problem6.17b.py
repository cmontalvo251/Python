import control as ctl
import matplotlib.pyplot as plt
import numpy as np


G1 = ctl.tf([1],[1,0,0])
print(G1)
G2 = ctl.tf([1,1],[1])
print(G2)
G3 = ctl.tf([1],[1,10])
print(G3)

GOL = G1*G2*G3

ctl.bode(G1,dB=True,label=str(G1))
ctl.bode(G2,dB=True,label=str(G2))
ctl.bode(G3,dB=True,label=str(G3))
ctl.bode(GOL,dB=True)
plt.legend()

print(ctl.margin(GOL))

plt.show()