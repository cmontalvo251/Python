###Integrate an ordinary differential equation
#in MATLAB that's using the function ode45.
#in Python we're going to use the Scipy toolbox and odeint
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as I
import control as C
import scipy.signal as S
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

kps = np.linspace(-100,100,400)
kds = np.linspace(-100,100,400)

kp, kd = np.meshgrid(kps,kds, sparse=False, indexing='ij')

eqn1 = (3-4*kd)

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax1.plot_wireframe(kp,kd,eqn1/abs(eqn1))
plt.xlabel('kp')
plt.ylabel('kd')

eqn2 = (24-28*kd-4*kp)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
ax2.plot_wireframe(kp,kd,eqn2/abs(eqn2))
plt.xlabel('kp')
plt.ylabel('kd')


eqn3 = ((24-28*kd-4*kp)*(48+8*kd-28*kp) - (3-4*kd)*(8*kp+168*kd))/(24-28*kd-4*kp)

fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='3d')
ax3.plot_wireframe(kp,kd,eqn3/abs(eqn3))
plt.xlabel('kp')
plt.ylabel('kd')

eqn4 = (24-28*kd-4*kp)*(-(168*kp)*(24-28*kd-4*kp) + (8*kp+168*kd)*((24-28*kd-4*kp)*(48+8*kd-28*kp) - (3-4*kd)*(8*kp+168*kd))/(24-28*kd-4*kp))/((24-28*kd-4*kp)*(48+8*kd-28*kp) - (3-4*kd)*(8*kp+168*kd))

fig4 = plt.figure()
ax4 = fig4.add_subplot(111, projection='3d')
ax4.plot_wireframe(kp,kd,eqn4/abs(eqn4))
plt.xlabel('kp')
plt.ylabel('kd')

eqn5 = (168*kp)

fig5 = plt.figure()
ax5 = fig5.add_subplot(111, projection='3d')
ax5.plot_wireframe(kp,kd,eqn5/abs(eqn5))
plt.xlabel('kp')
plt.ylabel('kd')

##Final result. Add everything together. Whereever the function is equal to 6 is stable
fig6 = plt.figure()
ax6 = fig6.add_subplot(111, projection='3d')
ax6.plot_wireframe(kp,kd,eqn1/abs(eqn1)+eqn2/abs(eqn2)+eqn3/abs(eqn3)+eqn4/abs(eqn4)+eqn5/abs(eqn5))
plt.xlabel('kp')
plt.ylabel('kd')

plt.show()
