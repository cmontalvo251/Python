import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import control as ctl
# System parameters
F0 = 1000      # N
c = 50         # Ns/m
m = 1000       # kg
# Time vector
t = np.linspace(0, 200, 1000)
# Analytic solution from 
v_analytic = (F0/c) * (1 - np.exp(-c/m * t))
# Numerical integration
def eoms(v, t, F0, c, m):
    return (F0 - c*v)/m
v_numeric = odeint(eoms,0,t,args=(F0, c, m)).flatten()
# Laplace (transfer function) solution
num = [c/m]
den = [1, c/m]
system = ctl.tf(num, den)
t_laplace, v_laplace = ctl.step_response(system, T=t)
v_laplace *= F0/c  # scale for step input magnitude
# Plotting
plt.figure(figsize=(8,5))
plt.plot(t, v_analytic, label='Analytic Solution', lw=2)
plt.plot(t, v_numeric, '--', label='Numerical Integration', lw=2)
plt.plot(t_laplace, v_laplace, ':', label='Laplace Solution', lw=2)
plt.xlabel('Time [s]')
plt.ylabel('Velocity [m/s]')
plt.title('First Order System Response')
plt.legend()
plt.grid(True)
plt.show()