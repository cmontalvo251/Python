import control as ctl
import matplotlib.pyplot as plt
import numpy as np
m = 300
c = 50

G = ctl.tf([1],[m,c,0])
print(G)

tout = np.linspace(0,1000,10000)

C = 600.0

a = 12

H = ctl.tf([a],[1,a])
print(H)

GCL = ctl.minreal((C*G)/(1+C*G*H))
print(GCL)

tout,yout_closed_loop = ctl.step_response(GCL,tout)

plt.figure()
plt.plot(tout,yout_closed_loop)

plt.show()
