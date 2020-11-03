import numpy as np
import matplotlib.pyplot as plt


time = np.linspace(0,500,1000)

T0 = 1.0  ##celsius
Tf = 22.5

for t in range(10,400,50):
    #time_to_get_to_98percent = 400.0

    tau = t/3.912 ###time constant

    print('tau = ',tau)

    a = 1/tau

    Temperature = (T0-Tf)*np.exp(-a*time) + Tf

    ### find t st T(t) = 0.68*(Tf-T0) + T0

    ### 0.68*(Tf-T0) + T0 = (T0-Tf)*e(-at) + Tf

    ### 0.68*(Tf-T0) + (T0-Tf) = (T0-Tf)*e(-at)

    ### 1-0.68 = e(-at)

    ### 0.32 = e(-at)

    ### time to 68% = -ln(0.32)/a = -ln(0.32)*tau = 1.14*tau

    ### 0.02 = e(-at)

    ## time to 98% = -ln(0.02)/a = -ln(0.02)*tau = 3.912*tau

    ### 1.12 

    plt.plot(time,Temperature,label=str(tau))
    plt.grid()
plt.legend()
plt.show()