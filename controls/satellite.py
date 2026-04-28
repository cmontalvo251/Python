import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import control as ctl
# System parameters
F0 = 0.1      # N
J = 10       # kg*m^2
d = 0.5      # m
# Time vector
t = np.linspace(0, 20, 1000)
# Analytic solution from
theta_analytic = (F0*d/J)*t**2
# Numerical integration
def eoms(z, t, F0,d,J):
    theta = z[0]
    thetadot = z[1]
    thetaddot = (2*F0*d)/J
    return [thetadot, thetaddot]
numeric = odeint(eoms, [0, 0], t, args=(F0, d, J))
theta_numeric = numeric[:, 0]
# Laplace (transfer function) solution
num = [2*d/J]
den = [1, 0, 0]
system = ctl.tf(num, den)
t_laplace, theta_laplace = ctl.step_response(system, T=t)
theta_laplace *= F0  # scale for step input magnitude
# Plotting
plt.figure(figsize=(8,5))
plt.plot(t, theta_analytic, label='Analytic Solution', lw=2)
plt.plot(t, theta_numeric, '--', label='Numerical Integration', lw=2)
plt.plot(t_laplace, theta_laplace, ':', label='Laplace Solution', lw=2)
plt.xlabel('Time [s]')
plt.ylabel('Angle [rad]')
plt.title('Second Order System Angle Response')
plt.legend()
plt.grid(True)

# Pole-zero maps for v_system and x_system
def plot_pz(sys, title=None):
    p = ctl.poles(sys)
    z = ctl.zeros(sys)
    plt.figure(figsize=(6,6))
    # plot zeros (o) and poles (x)
    if z.size:
        plt.plot(np.real(z), np.imag(z), 'o', ms=10, label='Zeros')
    if p.size:
        plt.plot(np.real(p), np.imag(p), 'x', ms=10, label='Poles')
    plt.axhline(0, color='k', lw=0.5)
    plt.axvline(0, color='k', lw=0.5)
    plt.xlabel('Real')
    plt.ylabel('Imag')
    if title:
        plt.title(title)
    plt.legend()
    plt.grid(True)
    #plt.gca().set_aspect('equal', 'box')

plot_pz(system, 'Pole-Zero Map')
plt.show()