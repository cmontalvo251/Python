import control as ctl
import matplotlib.pyplot as plt

G1 = ctl.tf([1],[1,0])
G2 = ctl.tf([1],[0.1,1])
G3 = ctl.tf([1],[0.5,1])
print(G1)
print(G2)
print(G3)

ctl.bode(G1,dB=True,label='G1')
ctl.bode(G2,dB=True,label='G2')
ctl.bode(G3,dB=True,label='G3')
plt.legend()
ctl.bode(G1*G2*G3,dB=True)
plt.show()