import numpy as np
import math as M
import matplotlib.pyplot as plt

def fact(num):
    return M.factorial(int(num))

def ntaker(n,r):
    return fact(n)/(fact(r)*fact(n-r))

def prob(n,r,p):
    return ntaker(n,r)*(p**r)*(1-p)**(n-r)

###Problem 24
n = 4.
r = 4.
p = 0.95
print('P(4) = ',prob(n,r,p))

###Problem 32
n = 180.
p = 0.95
rvec = np.arange(0,181,1) #for a cool plot
rvec = np.arange(176,181,1) #For actual problem 
prob_total=0.0
prob_total_vec = np.linspace(0,1,len(rvec))
prob_vec = np.linspace(0,1,len(rvec))
ctr = 0 
for r in rvec:
    print('r = ',r)
    pr = prob(n,r,p)
    print('P(r) = ',pr)
    prob_vec[ctr] = pr
    prob_total+=pr
    prob_total_vec[ctr] = prob_total
    ctr+=1
print('P(r>175) = ',prob_total)

#plt.plot(prob_total_vec)
plt.plot(prob_vec)

plt.figure()
plt.plot(prob_total_vec)
plt.show()
