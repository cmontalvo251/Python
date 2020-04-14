import numpy as np

E = 5.8e9
L = 1.
A = .05

k = E*A/L

print(k)

F = 100*4.41

print(F)

x = F/k

print(x)

strain = x/L

print(strain)

S = 2.5
R1 = 100.
R2 = 100.
R3i = 100.
R4 = 100.
Vs = 5.
Vo = strain*Vs*R2*R3i/(R2+R3i)**2
print(Vo)

resolution = (5-0)/2**16

print(resolution)

N = np.log(5/strain)/np.log(2)
print(N)