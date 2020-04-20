import numpy as np

def magnitude(w):
    G = 1/(w*1j+10)
    Gstar = 1/(-w*1j+10)
    M = np.sqrt(G*Gstar)
    return M

def phase(w): ##def stands for definition
    phase_num = 0
    #SOH CAH TOA
    phase_den = (180/np.pi)*np.arctan(w/10)
    return (phase_num - phase_den)

w = 1000
print(magnitude(w))
print(phase(w))