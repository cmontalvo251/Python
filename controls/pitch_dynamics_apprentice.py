import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import control as ctl
# System parameters
rho = 0.00238 #slugs-ft^3
V = 65.6 #ft/s
c = 0.75 #ft
b = 4.92 #ft
S = b*c #ft^2
Cmq = -24.45
Cma = -2.19
Cmde = -1.15
Iyy = 0.09 #slug-ft^2
l1 = -rho*V**2*S*c*Cmq/(4*Iyy*V)
l2 = -rho*V**2*S*c*Cma/(2*Iyy)
kappa = -rho*V**2*S*c*Cmde/(2*Iyy)
#Calculate Natural frequency and damping
wn = np.sqrt(l2)
zeta = l1/(wn*2)
print('Wn = ',wn,'zeta = ',zeta)
#Analytic Solution
t = np.linspace(0,1,1000)
m = 1
c = l1
k = l2
F0 = kappa
A1 = np.cos(np.sqrt(4*m*k - c**2)/(2*m)*t)
A2 = (c/np.sqrt(4*m*k - c**2))*np.sin(np.sqrt(4*m*k - c**2)/(2*m)*t)
theta_analytic = (F0/k)*(1 - np.exp(-c/(2*m)*t)*(A1 + A2))
# Numerical integration
def eoms(z, t, kappa,l1,l2):
    theta = z[0]
    thetadot = z[1]
    thetaddot = kappa - l1*thetadot - l2*theta
    return [thetadot, thetaddot]
numeric = odeint(eoms, [0, 0], t, args=(kappa,l1,l2))
theta_numeric = numeric[:, 0]
# Laplace (transfer function) solution
num = [kappa]
den = [1, l1, l2]
system = ctl.tf(num, den)
t_laplace, theta_laplace = ctl.step_response(system, T=t)
# Plotting
plt.figure(figsize=(8,5))
plt.plot(t,theta_analytic, label='Analytic Solution', lw=2)
plt.plot(t,theta_numeric, '--', label='Numerical Integration', lw=2)
plt.plot(t_laplace, theta_laplace, ':', label='Laplace Solution', lw=2)
plt.xlabel('Time [s]')
plt.ylabel('Theta (rad)')
plt.title('Aircraft Pitch Response')
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