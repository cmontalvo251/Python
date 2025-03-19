import numpy as np
import matplotlib.pyplot as plt

names = ['pitotraw.txt','pitotraw.txt','pitotraw.txt']

for name in names:
    data = np.loadtxt(name)
    time = data[:,0]
    Do = data[:,1]
    time-=time[0]

    v = 3.3*Do/2**16
    vref = v[0]
    dv = v-vref
    dP = dv*1000
    dP[dP<0] = 0
    U = np.sqrt(2*dP/1.225)

    m = np.where(U>5)[0][0]
    print(m,time[m])

    ## Uf(i+1) = ( Uf(i) + U(i) ) / 2
    Uf = 0*U
    Uf[0] = U[0]
    s = 0.75
    for i in range(0,len(U)-1):
        #Uf[i+1] = ( Uf[i] + U[i] ) / 2
        Uf[i+1] = s*Uf[i] + (1-s)*U[i]
    plt.figure()
    plt.plot(time[2:m],U[2:m])
    #plt.plot(time[:m],Uf[2:m])


    xbar = np.mean(U[2:m])
    print('xbar = ',xbar)
    S = np.std(U[2:m])
    print('Standard Deviation = ',S)
    plt.figure()
    hist_data = plt.hist(U[2:m])
    print(hist_data)
    bins = hist_data[0]
    max_count = np.max(bins)

    xg = np.linspace(np.min(U[2:m]),np.max(U[2:m]),1000)
    yg = 1/(np.sqrt(2*np.pi)*S)*np.exp(-(xg-xbar)**2/(2*S**2)) 
    ygmax = np.max(yg)
    yg *= max_count / ygmax
    plt.plot(xg,yg)

plt.show()
