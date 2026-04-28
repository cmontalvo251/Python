import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import control as ctl
# System parameters
rho = 0.00238
V = 150.0
d = 1.0
a = 3*d
T = 10
b = 6
W = 6.0
J = (W/32.2)/12*(d**2 + b**2)
print('J = ',J)
lam = np.pi/(J*8)*rho*V**2*d**2*a
kappa = T*b/(2*J)
# Time vector
t = np.linspace(0, 5, 1000)
# Analytic solution
m = 1
k = lam
c = 0
F0 = kappa
A1 = np.cos(np.sqrt(4*m*k - c**2)/(2*m)*t)
A2 = (c/np.sqrt(4*m*k - c**2))*np.sin(np.sqrt(4*m*k - c**2)/(2*m)*t)
theta_analytic = (F0/k)*(1 - np.exp(-c/(2*m)*t)*(A1 + A2))
# Numerical integration
def eoms(z, t, kappa,lam):
    theta = z[0]
    thetadot = z[1]
    thetaddot = kappa - lam*theta
    return [thetadot, thetaddot]
numeric = odeint(eoms, [0, 0], t, args=(kappa,lam))
theta_numeric = numeric[:, 0]
# Laplace (transfer function) solution
num = [kappa]
den = [1, 0,lam]
system = ctl.tf(num, den)
t_laplace, theta_laplace = ctl.step_response(system, T=t)
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
