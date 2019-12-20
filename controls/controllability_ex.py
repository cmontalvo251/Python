import control as ctl
import numpy as np

k = 10.
c = 5.
A = np.asarray([[0,1,0,0],[-k,-c,0,0],[0,0,0,1],[0,0,-2*k,-2*c]])
B = np.asarray([[0],[1],[0],[0]])
C = np.asarray([1,0,0,0])
D = 0

sys = ctl.StateSpace(A,B,C,D)

Wc = ctl.gram(sys,'c')

rank = np.linalg.matrix_rank(Wc)

print('r = ',rank)

[s,v] = np.linalg.eig(A)

#Check for mode controllability
Ap = A-s[2]*np.eye(4)
mode_test_matrix = np.concatenate((Ap,B),axis=1)
rank_test = np.linalg.matrix_rank(mode_test_matrix)
print('r_test = ',rank_test)
