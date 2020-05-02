import control as ctl
import numpy as np
import sys

k = 10.
c = 2.

##1D Problem
A = np.asarray([[0,1],[-k,-c]])
B = np.asarray([[0],[1]])
C = np.asarray([1,0])
D = 0 
sysSS = ctl.StateSpace(A,B,C,D)
tf = ctl.ss2tf(sysSS)
print(tf)
print(ctl.pole(tf))
Wc = ctl.gram(sysSS,'c')
rank = np.linalg.matrix_rank(Wc)
print('r = ',rank)
[s,v] = np.linalg.eig(A)


#Check for mode controllability
Ap = A-s[1]*np.eye(2)
mode_test_matrix = np.concatenate((Ap,B),axis=1)
rank_test = np.linalg.matrix_rank(mode_test_matrix)
print('r_test = ',rank_test)

print('2D System')
A = np.asarray([[0,1,0,0],[-2*k,2*-c,k,c],[0,0,0,1],[k,c,-2*k,-2*c]])
#B = np.asarray([[0],[1],[0],[1]])
B = np.asarray([[0,0],[1,0],[0,0],[0,1]])
C = np.asarray([1,0,0,0])
D = 0
[s,v] = np.linalg.eig(A)

#sysSS = ctl.StateSpace(A,B,C,D)
#Wc = ctl.gram(sysSS,'c')
Wc = ctl.ctrb(A,B)
rank = np.linalg.matrix_rank(Wc)
print('r = ',rank)


#Check for mode controllability
Ap = A-s[3]*np.eye(4)
mode_test_matrix = np.concatenate((Ap,B),axis=1)
rank_test = np.linalg.matrix_rank(mode_test_matrix)
print('r_test = ',rank_test)
