import control as ctl
import matplotlib.pyplot as plt
import numpy as np


G1 = ctl.tf([1],[1,0,0])
print(G1)
G3 = ctl.tf([1,1],[1])*ctl.tf([1,1],[1])
print(G3)
G2= ctl.tf([1],[1,10])
print(G2)

GOL = G1*G2*G3

ctl.bode(G1,dB=True,label=str(G1))
ctl.bode(G2,dB=True,label=str(G2))
ctl.bode(G3,dB=True,label=str(G3))
ctl.bode(GOL,dB=True)
plt.legend()

gm,pm,wg,wp = ctl.margin(GOL)
print('My Gain Margin in Magnitude = ',gm)
gmdB = 20*np.log10(gm)
print('My Gain Margin in dB = ',gmdB)

ctl.rlocus(GOL)

plt.figure()
for k in np.linspace(0.1,10,100):
    s = ctl.pole(k*GOL/(1+k*GOL))
    plt.plot(np.real(s),np.imag(s),'b*')
plt.grid()
k = 9
s = ctl.pole(ctl.minreal(k*GOL/(1+k*GOL)))
plt.plot(np.real(s),np.imag(s),'r*')

GCL = k*GOL/(1+k*GOL)
tout = np.linspace(0,10,1000)
tout,yout = ctl.step_response(GCL,tout)
plt.figure()
plt.plot(tout,yout)
plt.grid()

plt.show()