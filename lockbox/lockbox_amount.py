import numpy as np
import matplotlib.pyplot as plt

def ntakek(n,k):
    return np.math.factorial(n)/(np.math.factorial(k)*np.math.factorial(n-k))

##give me 
k_vec = []
amount_vec = []
n = 11 #number of digits
total_amount = 0
for k in range(1,n+1):
    k_vec.append(k)
    amount = ntakek(n,k)
    total_amount+=amount
    print(k,amount)
    amount_vec.append(amount)
plt.plot(k_vec,amount_vec)
print('Total Amount = ',total_amount)
plt.show()
