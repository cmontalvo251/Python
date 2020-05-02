import control as ctl
import matplotlib.pyplot as plt
import numpy as np

sig = 10

G1 = ctl.tf([sig],[1,sig])
G2 = G1
#K(s+a)
C = ctl.tf([1,3],[1])

#print(G1)
#print(G2)
#print(G3)

#wc = 1000
#G4 = ctl.tf([wc],[1,wc])

GOL = C*G1*G2

ctl.bode(G1,dB=True,label='G1')
ctl.bode(G2,dB=True,label='G2')
ctl.bode(C,dB=True,label='C')
ctl.bode(GOL,dB=True)
plt.legend()
gm,pm,wg,wp = ctl.margin(GOL)
print('My Gain Margin in Magnitude = ',gm)
gmdB = 20*np.log10(gm)
print('My Gain Margin in dB = ',gmdB)
plt.figure()

## 1 + K*L = 0 ,,  L = GOL
## K*L  = -180 , abs(1) which corresponds to 180 deg phase and dB = 0
## K = 8 cross 0 dB at -180 and be unstable
# K < 8

for k in np.linspace(0.1,10,100):
    s = ctl.pole(k*GOL/(1+k*GOL))
    plt.plot(np.real(s),np.imag(s),'b*')
plt.grid()
k = 7.5
s = ctl.pole(k*GOL/(1+k*GOL))
plt.plot(np.real(s),np.imag(s),'r*')

GCL = k*GOL/(1+k*GOL)
tout = np.linspace(0,10,1000)
tout,yout = ctl.step_response(GCL,tout)
plt.figure()
plt.plot(tout,yout)
plt.grid()

ctl.rlocus(GOL)

plt.show()