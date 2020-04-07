import control as ctl
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

N,D = sig.zpk2tf([-2],[0,2,-1+3j,-1-3j],1)
G = ctl.tf(N,D)
print(G)
ctl.rlocus(G)
plt.show()