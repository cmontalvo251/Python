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
x_analytic = (F0/c)*t + (F0*m/c**2)*(np.exp(-c/m*t)-1)
# Numerical integration
def eoms(z, t, F0, c, m):
    x = z[0]
    v = z[1]
    xdot = v
    xddot = (F0 - c*v)/m
    return [xdot, xddot]
numeric = odeint(eoms, [0, 0], t, args=(F0, c, m))
v_numeric = numeric[:, 1]
x_numeric = numeric[:, 0]
# Laplace (transfer function) solution
num = [c/m]
den = [1, c/m]
v_system = ctl.tf(num, den)
x_system = ctl.tf(num, [1, c/m, 0]) #notice the extra zero for position
t_laplace, v_laplace = ctl.step_response(v_system, T=t)
t_laplace, x_laplace = ctl.step_response(x_system, T=t)
v_laplace *= F0/c  # scale for step input magnitude
x_laplace *= F0/c  # scale for step input magnitude
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

plt.figure(figsize=(8,5))
plt.plot(t, x_analytic, label='Analytic Solution', lw=2)
plt.plot(t, x_numeric,label='Numerical Integration', lw=2)
plt.plot(t_laplace, x_laplace, ':', label='Laplace Solution', lw=2)
plt.xlabel('Time [s]')
plt.ylabel('Position [m]')
plt.title('Second Order System Position Response (ω_n=0)')
plt.grid(True)
plt.show()