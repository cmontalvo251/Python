import control as C
import matplotlib.pyplot as plt
import numpy as np

tout = np.linspace(0,10,1000)

AoA_open_loop = C.tf([3],[1,4,4])

tout,aoa_out = C.step_response(AoA_open_loop,tout)

plt.plot(tout,aoa_out)

altitude_open_loop = C.tf([-1,-4,14],[3,0,0])
tout,altitude_out = C.step_response(altitude_open_loop,tout)

plt.figure()
plt.plot(tout,altitude_out)

aoa_closed_loop = C.tf([4,12],[1,8,16])

tout,aoa_closed_out = C.step_response(aoa_closed_loop,tout)

plt.figure()
plt.plot(tout,aoa_closed_out)

kp = -10
ki = 0.001

num_closed_shit = [-4*kp,-4*ki-28*kp,8*kp-28*ki,8*ki+168*kp,168*ki]
den_closed_shit = [3,24-4*kp,48-4*ki-28*kp,8*kp-28*ki,8*ki+168*kp,168*ki]

roots_are = np.roots(den_closed_shit)

print(roots_are)

altitude_closed_loop = C.tf(num_closed_shit,den_closed_shit)

tout,altitude_closed_out = C.step_response(altitude_closed_loop,tout)

plt.figure()
plt.plot(tout,altitude_closed_out)

plt.show()