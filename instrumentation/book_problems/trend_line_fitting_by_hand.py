import numpy as np
import matplotlib.pyplot as plt

Y = np.asarray([250,200,150,75,0])
X = np.asarray([5.0,4.2,3.0,1.4,0.8])

H = np.asarray([[len(X),np.sum(X)],[np.sum(X),np.sum(X**2)]])

print(H)

Hinv = np.linalg.inv(H)

print(Hinv)

HY = np.asarray([np.sum(Y),np.sum(X*Y)])

print(HY)

thetastar = np.matmul(Hinv,HY)

print(thetastar)

##Quadratic

H2 = np.asarray([[np.sum(X**4),np.sum(X**3),np.sum(X**2)],[np.sum(X**3),np.sum(X**2),np.sum(X)],[np.sum(X**2),np.sum(X),len(X)]])
print(H2)
H2inv = np.linalg.inv(H2)

HY2 = np.asarray([np.sum(X**2*Y),np.sum(X*Y),np.sum(Y)])

print(HY2)

thetastar2 = np.matmul(H2inv,HY2)

print(thetastar2)

Wbar = np.mean(Y)

print(Wbar)

Ylinear = X*thetastar[1] + thetastar[0]
Yfamily = 2.8*thetastar[1] + thetastar[0]

print(Ylinear)

Yquadratic = thetastar2[0]*X**2 + thetastar2[1]*X + thetastar2[2]
Yfamily2 = thetastar2[0]*(2.8)**2 + thetastar2[1]*2.8 + thetastar2[2]

print(Yquadratic)

dY = (Y-Wbar)
a = np.sum(dY**2)

r2linear = 1 - np.sum((Ylinear-Y)**2)/a
r2quadratic = 1 - np.sum((Yquadratic-Y)**2)/a

print(r2linear)
print(r2quadratic)

plt.plot(X,Y,'b*')
plt.plot(X,Ylinear,'r-')
plt.plot(X,Yquadratic,'g-')
plt.show()