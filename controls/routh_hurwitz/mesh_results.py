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

kps = np.linspace(-100,100,200)
kis = np.linspace(-100,100,200)

kp, ki = np.meshgrid(kps,kis, sparse=False, indexing='ij')

eqn1 = 3.0 ##trivial no need to plot

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax1.plot(kp,ki,eqn1/abs(eqn1))

eqn2 = (24.-4.*kp)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
ax2.plot_wireframe(kp,ki,eqn2/abs(eqn2))
plt.xlabel('kp')
plt.ylabel('ki')

eqn3 = ((24.-4.*kp)*(48.-4.*ki-28.*kp) - 3.0*(8.*kp-28.*ki))/(24.-4.*kp)

fig3 = plt.figure()
ax3 = fig3.add_subplot(111, projection='3d')
ax3.plot_wireframe(kp,ki,eqn3/abs(eqn3))
plt.xlabel('kp')
plt.ylabel('ki')

eqn4 = (24-4*kp)*(3.0*(168*ki) - (24-4*kp)*(8*ki+168*kp) + (8*kp-28*ki)*((24-4*kp)*(48-4*ki-28*kp) - 3.0*(8*kp-28*ki))/(24-4*kp))/((24-4*kp)*(48-4*ki-28*kp) - 3.0*(8*kp-28*ki))      

fig4 = plt.figure()
ax4 = fig4.add_subplot(111, projection='3d')
ax4.plot_wireframe(kp,ki,eqn4/abs(eqn4))
plt.xlabel('kp')
plt.ylabel('ki')

eqn5 = ((24-4*kp)*(48-4*ki-28*kp) - 3.0*(8*kp-28*ki))*(-(168*ki)*((24-4*kp)*(48-4*ki-28*kp) - 3.0*(8*kp-28*ki))/(24-4*kp) + (-3.0*(168*ki) + (24-4*kp)*(8*ki+168*kp))*(3.0*(168*ki) - (24-4*kp)*(8*ki+168*kp) + (8*kp-28*ki)*((24-4*kp)*(48-4*ki-28*kp) - 3.0*(8*kp-28*ki))/(24-4*kp))/((24-4*kp)*(48-4*ki-28*kp) - 3.0*(8*kp-28*ki)))/((24-4*kp)*(3.0*(168*ki) - (24-4*kp)*(8*ki+168*kp) + (8*kp-28*ki)*((24-4*kp)*(48-4*ki-28*kp) - 3.0*(8*kp-28*ki))/(24-4*kp)))

fig5 = plt.figure()
ax5 = fig5.add_subplot(111, projection='3d')
ax5.plot_wireframe(kp,ki,eqn5/abs(eqn5))
plt.xlabel('kp')
plt.ylabel('ki')

eqn6 = 168*ki

fig6 = plt.figure()
ax6 = fig6.add_subplot(111, projection='3d')
ax6.plot_wireframe(kp,ki,eqn6/abs(eqn6))
plt.xlabel('kp')
plt.ylabel('ki')

##Final result. Add everything together. Whereever the function is equal to 6 is stable
fig7 = plt.figure()
ax7 = fig7.add_subplot(111, projection='3d')
ax7.plot_wireframe(kp,ki,eqn1/abs(eqn1)+eqn2/abs(eqn2)+eqn3/abs(eqn3)+eqn4/abs(eqn4)+eqn5/abs(eqn5)+eqn6/abs(eqn6))
plt.xlabel('kp')
plt.ylabel('ki')

plt.show()
