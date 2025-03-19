import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy import stats

def ntakek(n,k):
    return np.math.factorial(n)/(np.math.factorial(k)*np.math.factorial(n-k))
Total_Prob = 0
n = 5
p = 3.84/100
for k in range(0,n+1):
    #print(i)
    Prob = ntakek(n,k)*(p**k)*(1-p)**(n-k)
    Total_Prob += Prob
    if k == 0:
        print('Answer = ',1-Prob)
    print(k,Prob*100)
print(Total_Prob)
