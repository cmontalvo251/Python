import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import control as ctl
# System parameters
F0 = 1000      # N
k = 2000       # N/m
c = 50         # Ns/m
m = 100       # kg
# Time vector
t = np.linspace(0, 20, 1000)
# Analytic solution from
A1 = np.cos(np.sqrt(4*m*k - c**2)/(2*m)*t)
A2 = (c/np.sqrt(4*m*k - c**2))*np.sin(np.sqrt(4*m*k - c**2)/(2*m)*t)
x_analytic = (F0/k)*(1 - np.exp(-c/(2*m)*t)*(A1 + A2))
# Numerical integration
def eoms(z, t, F0, c, m,k):
    x = z[0]
    xdot = z[1]
    xddot = (F0 - c*xdot - k*x)/m
    return [xdot, xddot]
numeric = odeint(eoms, [0, 0], t, args=(F0, c, m,k))
x_numeric = numeric[:, 0]
# Laplace (transfer function) solution
num = [k/m]
den = [1, c/m, k/m]
system = ctl.tf(num, den)
t_laplace, x_laplace = ctl.step_response(system, T=t)
x_laplace *= F0/k  # scale for step input magnitude
# Plotting
plt.figure(figsize=(8,5))
plt.plot(t, x_analytic, label='Analytic Solution', lw=2)
plt.plot(t, x_numeric, '--', label='Numerical Integration', lw=2)
plt.plot(t_laplace, x_laplace, ':', label='Laplace Solution', lw=2)
plt.xlabel('Time [s]')
plt.ylabel('Position [m]')
plt.title('Second Order System Position Response')
plt.legend()
plt.grid(True)
plt.show()