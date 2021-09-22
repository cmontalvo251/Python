import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy import stats

def ntakek(n,k):
    return np.math.factorial(n)/(np.math.factorial(k)*np.math.factorial(n-k))
n_vec = []
p_vec = []
for n in range(100,200):
    n_vec.append(n)
    print(n)# = 185
    p = 0.05
    Total_Prob = 0
    for i in range(0,n-175):
        #print(i)
        Prob = ntakek(n,i)*(p**i)*(1-p)**(n-i)
        Total_Prob += Prob
    print(Total_Prob)
    p_vec.append(Total_Prob)
plt.plot(n_vec,p_vec)
plt.show()