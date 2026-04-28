##90% of the code created by ChatGPT - Spring 2025
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parameters of the mass-spring-damper system
m = 1.0  # Mass (kg)
c = 0.0  # Damping coefficient (Ns/m)
k = 4.0*np.pi**2  # Spring constant (N/m)

# Define the system of first-order ODEs
def model(y, t, m, c, k):
    x1, x2 = y  # Unpack the state vector (displacement and velocity)
    dx1dt = x2  # dx1/dt = velocity
    F = 0.0
    dx2dt = -(c/m) * x2 - (k/m) * x1 + F/m  # dx2/dt = acceleration
    return [dx1dt, dx2dt]

# Initial conditions
x1_0 = 1.0  # Initial displacement (m)
x2_0 = 0.0  # Initial velocity (m/s)

y0 = [x1_0, x2_0]  # Initial state vector

# Time vector
t = np.linspace(0, 10, 1000)  # Simulate from t=0 to t=10 seconds

# Solve the ODE using odeint
solution = odeint(model, y0, t, args=(m, c, k))

# Extract the displacement and velocity from the solution
displacement = solution[:, 0]
velocity = solution[:, 1]

# Plot the results
plt.plot(t, displacement,'b-',label='Simulated Data')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.title('Mass-Spring-Damper System - Displacement')
plt.grid()

##WE ARE GOING TO ADD OUR EQUATION ON TOP
"""
tf = np.linspace(0, 10, 1000)
a0 = 0
af = 5.0
ts = 17.5
tau = ts/4
s = 1/tau
T = 6.54-2.0
f = 1/T
wd = 2*np.pi*f
wn = np.sqrt(wd**2 - s**2)
print('Wn = ',wn)
zeta = s/wn
print('damping ratio = ',zeta)
a = af + np.exp(-s*tf)*(a0-af)*np.cos(wd*tf)
plt.plot(tf,a,'b-',label='Simulated Fit')
"""

###SAMPLE THE DATA
wn = np.sqrt(k/m)
f = wn/(2*np.pi)
fs = 2*f
Ts = 1/fs
ts = np.arange(0.3,10,Ts)
sampled_data = 1.0*np.cos(wn*(ts))
plt.plot(ts,sampled_data,'r-*',label='Sampled Data')
plt.legend()

plt.show()
