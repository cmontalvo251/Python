import numpy as np
import control as ctl
import matplotlib.pyplot as plt

a = 5
G = ctl.tf([a],[1,a])
print(G)

"""Let's hit this with an input"""
w = a
U = ctl.tf([w],[1,0,w**2])
print(U)

Y = G*U
tout = np.linspace(0,100,10000)
tout,yout = ctl.impulse_response(Y,tout)
u = np.sin(w*tout)
plt.plot(tout,yout,label='Y')
plt.plot(tout,u,label='U')
plt.legend()
plt.grid()

plt.figure()
ctl.bode(G,dB=True)

plt.show()
