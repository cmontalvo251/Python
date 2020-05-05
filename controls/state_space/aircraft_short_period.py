import control as ctl
import numpy as np
import matplotlib.pyplot as plt

A = np.asarray([[-0.6,223.20],[-0.0093,-0.51]])

poles,vectors = np.linalg.eig(A)

print(poles)

char_poly_roots = np.roots([1,1.11,2.38])

print(char_poly_roots)

## ak = b
a = np.asarray([[10.84,2.09],[472.018,1.153]])
b = np.asarray([8.09,18.78])
k = np.matmul(np.linalg.inv(a),b)
print(k)

##Check Atilde = A+B*k
K = np.matrix(k)
B = np.matrix([[-10.84],[-2.09]])
BK = np.matmul(B,K)
print('BK=',BK)
Atilde = A+BK
print('Atilde=',Atilde)
poles,vectors = np.linalg.eig(Atilde)
print(poles)