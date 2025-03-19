import numpy as np
import math
import matplotlib.pyplot as plt

def fact(num):
    return math.factorial(num)

def ntaker(n,r):
    return fact(n)/(fact(r)*fact(n-r))

def prob(n,r,p):
    return ntaker(n,r)*(p**r)*(1-p)**(n-r)

p = 1.0/365.

n = 2
Ptot = 0
for r in range(0,n+1):
    pr = prob(n,r,p)
    Ptot += pr
    print(r,pr)
print('P total = ',Ptot)

##Birthday twin problem goes like this
## P(r >= 1 ) = 1- P(r = 0)
# loop through number of students in class
for n in range(1,100):
    print('P = ',1-prob(n,0,p),' Students = ',n)