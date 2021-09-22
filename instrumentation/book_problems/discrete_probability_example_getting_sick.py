import numpy as np
import matplotlib.pyplot as plt
import math as M
N = np.arange(0,200,1)
p = 0.05
Pnotgetsick = (1-p)**N
Pgettingsickonthelasttime = (1-p)**(N-1)*p
print(N)
print(Pnotgetsick)
print(Pgettingsickonthelasttime)

#N = np.log(0.5)/np.log(0.95)

def ntaker(n,r):
    return M.factorial(n)/(M.factorial(r)*M.factorial(n-r))

def binomial(n,r,p):
    return ntaker(n,r)*(p**r)*(1-p)**(n-r)

n = 14
p = 0.05
PIwillnotgetsick = binomial(n,0,p)
print(PIwillnotgetsick)